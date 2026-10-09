import os
from dotenv import load_dotenv

load_dotenv()

from app.services.rag_service import rag_service

PDF_FILE = "Markov chains.pdf"

if __name__ == "__main__":
    if os.path.exists(PDF_FILE):
        print("1. PDF Indexelése (csak egyszer fut le élesben)...")
        ingest_result = rag_service.ingest_pdf(PDF_FILE)
        print(ingest_result.message)

        print("\n2. Kérdezés tesztelése...")
        while True:
            user_question = input("\nKérdés: ")
            if user_question.lower() in ["exit", "quit"]:
                break
            if user_question.strip():
                result = rag_service.answer_query(user_question)
                print("\n--- VÁLASZ ---")
                print(result.answer)
                print("\n--- FORRÁSOK ---")
                for src in result.sources:
                    print(f"• Oldal: {src.page} | Részlet: {src.page_content[:80]}...")