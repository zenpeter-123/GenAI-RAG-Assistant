import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

from app.core.config import settings
from app.models.schemas import QueryResponse, SourceDocument, IngestResponse


class RAGService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            api_key=settings.OPENAI_API_KEY
        )
        self.persist_directory = settings.CHROMA_PERSIST_DIR
        self.llm = ChatOpenAI(
            model=settings.DEFAULT_MODEL,
            temperature=0,
            api_key=settings.OPENAI_API_KEY
        )
        
        self.vectorstore = Chroma(
            collection_name="enterprise_pdf_rag",
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        # A chunkok tárolása a BM25-höz
        self.all_chunks = []

    def ingest_pdf(self, pdf_path: str) -> IngestResponse:
        """PDF feldolgozása, darabolása és elmentése az adatbázisba."""
        filename = os.path.basename(pdf_path)
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150
        )
        chunks = text_splitter.split_documents(docs)

        # Metadata: forrás hozzáadása
        for chunk in chunks:
            chunk.metadata["source"] = filename

        # Hozzáadás a vektoros tárolóhoz
        self.vectorstore.add_documents(chunks)

        # Hozzáadás a BM25-höz
        self.all_chunks.extend(chunks)

        return IngestResponse(
            filename=filename,
            num_chunks=len(chunks),
            message=f"Sikeresen indexelve {len(chunks)} szövegblokk."
        )

    def answer_query(self, question: str, top_k: int = 3) -> QueryResponse:
        """Kérdés megválaszolása hybrid kereséssel, reranker nélkül."""
        
        # 1. Vektoros retriever
        vector_retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": top_k * 3}
        )
        
        # 2. BM25 retriever
        bm25_retriever = BM25Retriever.from_documents(self.all_chunks)
        bm25_retriever.k = top_k * 3
        
        # 3. Ensemble retriever
        ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, vector_retriever],
            weights=[0.5, 0.5]
        )
        
        # 4. Keresés
        relevant_docs = ensemble_retriever.invoke(question)
        
        # 5. Csak a top_k legjobbat tartjuk meg
        relevant_docs = relevant_docs[:top_k]

        # 6. Kontextus összeállítása
        context = "\n\n".join([doc.page_content for doc in relevant_docs])

        # 7. Prompt
        prompt_template = ChatPromptTemplate.from_template(
            """Válaszolj az alábbi kérdésre kizárólag a megadott kontextus alapján. 
Ha a válasz nem található meg a kontextusban, mondd azt, hogy "Nem található elegendő információ a dokumentumban."

Kontextus:
{context}

Kérdés:
{question}
"""
        )

        chain = prompt_template | self.llm
        response = chain.invoke({"context": context, "question": question})

        # 8. Források
        sources = [
            SourceDocument(
                page_content=doc.page_content[:200] + "...",
                page=doc.metadata.get("page", None),
                source=doc.metadata.get("source", None)
            )
            for doc in relevant_docs
        ]

        return QueryResponse(
            question=question,
            answer=response.content,
            sources=sources
        )


rag_service = RAGService()