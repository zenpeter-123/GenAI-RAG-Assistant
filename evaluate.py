from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

evaluation_questions = [
    "Mi a RAG asszisztens alapvető célja a dokumentum szerint?",
    "Hány dimenziós valós vektorteret (d) használ az OpenAI modellje?",
    "Hova történik a pontok vetítése ebben a vektortér-konstrukcióban?",
    "Pontosan hogyan van definiálva az u és v vektorok közötti távolságmennyiség d(u,v)?",
    "Mitől függ a skaláris szorzat értéke ebben a gömbi távolság-modellben?",
    "Mi a pontos célja az embedding modellnek a válaszok és kérdések egységgömbre vetítése mögött?",
    "Melyik tudományos cikk foglalkozik a kontrasztív reprezentációtanulással a hiperszférán?",
    "A kérdés gömbfelszíni vetületéhez viszonyítva hány legközelebb eső válasz vetületét határozzuk meg?",
    "Hogyan osztja le a szerepeket a rendszer a ChromaDB és a nyelvi modell között?",
    "Mi a RAG (Retrieval Augmentation Generation) folyamat pontos lépésről lépésre láncolata?",
    "Mely alapvető Python könyvtárakat kell letölteni a virtuális környezetbe az implementáció első lépéseként?",
    "Milyen konkrét funkciót biztosít a jelenlegi projekt FastAPI endpointos megoldása?",
    "Milyen típusú tokeneket/modellt használ az LLM rész az implementáció megvalósításához?",
    "Hogyan biztosítható, hogy a válaszok ne torzuljanak az egységgömbre vetítés közben?",
    "Ki a szerzője és mi a címe a bibliográfiában szereplő 2020-as hivatkozásnak?"
]

def run_evaluation():
    print("=== RAG SYSTEM AUTOMATED EVALUATION ===")
    
    # 1. Lépés: Először feltöltjük és indexeljük a PDF-et a /upload végponton keresztül
    # (Győződj meg róla, hogy a 'project_documentation.pdf' ott van a projekt gyökerében!)
    pdf_filename = "project_documentation.pdf"
    
    if os.path.exists(pdf_filename):
        print(f"Dokumentum feltöltése és indexelése: {pdf_filename}...")
        with open(pdf_filename, "rb") as f:
            upload_response = client.post(
                "/api/v1/upload", 
                files={"file": (pdf_filename, f, "application/pdf")}
            )
        
        if upload_response.status_code == 201:
            print("Sikeres feltöltés és indexelés!\n")
        else:
            print(f"Hiba a feltöltés során: {upload_response.status_code} - {upload_response.text}")
            return
    else:
        print(f"Figyelem: A {pdf_filename} nem található a gyökérben! Kérlek, másold oda a teszteléshez.")
        return

    # 2. Lépés: Futtatjuk a 15 kérdést a /chat végponton
    success_count = 0
    for i, question in enumerate(evaluation_questions, 1):
        print(f"\n[Test {i}/15] Kérdés: {question}")
        
        response = client.post("/api/v1/chat", json={"question": question, "top_k": 3})
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", data.get("response", str(data)))
            print(f"Válasz: {answer[:300]}...") 
            success_count += 1
        else:
            print(f"Hiba! Státuszkód: {response.status_code}, Válasz: {response.text}")
            
    print(f"\nEvaluáció kész! Sikeresen lekérdezve: {success_count}/15 tesztkérdés.")

if __name__ == "__main__":
    run_evaluation()