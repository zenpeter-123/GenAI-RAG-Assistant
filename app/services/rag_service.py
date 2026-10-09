import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate

from app.core.config import settings
from app.models.schemas import QueryResponse, SourceDocument, IngestResponse

class RAGService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL, api_key=settings.OPENAI_API_KEY)
        self.persist_directory = settings.CHROMA_PERSIST_DIR
        self.llm = ChatOpenAI(model=settings.DEFAULT_MODEL, temperature=0, api_key=settings.OPENAI_API_KEY)
        
        # Perszisztens ChromaDB betöltése/létrehozása
        self.vectorstore = Chroma(
            collection_name="enterprise_pdf_rag",
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

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

        # Adatok hozzáadása a perszisztens tárolóhoz
        self.vectorstore.add_documents(chunks)
        
        return IngestResponse(
            filename=filename,
            num_chunks=len(chunks),
            message=f"Sikeresen indexelve {len(chunks)} szövegblokk."
        )

    def answer_query(self, question: str, top_k: int = 3) -> QueryResponse:
        """Kérdés megválaszolása a tárolott vektorok alapján, forrásmegjelöléssel."""
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": top_k})
        relevant_docs = retriever.invoke(question)

        context = "\n\n".join([doc.page_content for doc in relevant_docs])

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

        # Források kinyerése oldalszámokkal
        sources = [
            SourceDocument(
                page_content=doc.page_content[:200] + "...",  # Csak az eleje kivonatként
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