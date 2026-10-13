import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()  # Hivatalos, szinkron OpenAI kliens

def evaluate_rag(question: str, answer: str, context: str):
    print("Értékelés indítása gpt-4o-mini-vel...\n")

    # 1. Faithfulness (Hűség) mérése
    faithfulness_prompt = f"""
    Feladatod egy RAG rendszer válaszának értékelése.
    
    Kontextus: {context}
    Válasz: {answer}
    
    Határozd meg, hogy a válaszban szereplő állítások teljesen alátámaszthatók-e a megadott kontextus alapján!
    
    Válaszolj kizárólag érvényes JSON formátumban:
    {{
        "score": <0.0 és 1.0 közötti pontszám>,
        "reason": "<Rövid indoklás magyarul>"
    }}
    """

    # 2. Answer Relevancy (Relevancia) mérése
    relevancy_prompt = f"""
    Feladatod egy RAG rendszer válaszának értékelése.
    
    Kérdés: {question}
    Válasz: {answer}
    
    Határozd meg, hogy a válasz mennyire releváns és közvetlen a feltett kérdésre!
    
    Válaszolj kizárólag érvényes JSON formátumban:
    {{
        "score": <0.0 és 1.0 közötti pontszám>,
        "reason": "<Rövid indoklás magyarul>"
    }}
    """

    # Hívás 1: Faithfulness
    res_f = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": faithfulness_prompt}],
        response_format={"type": "json_object"}
    )
    faithfulness_result = json.loads(res_f.choices[0].message.content)

    # Hívás 2: Answer Relevancy
    res_r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": relevancy_prompt}],
        response_format={"type": "json_object"}
    )
    relevancy_result = json.loads(res_r.choices[0].message.content)

    # Eredmények kiíratása
    print("--- Faithfulness (Hűség) ---")
    print(f"Pontszám: {faithfulness_result.get('score')}")
    print(f"Indoklás: {faithfulness_result.get('reason')}\n")

    print("--- Answer Relevancy (Relevancia) ---")
    print(f"Pontszám: {relevancy_result.get('score')}")
    print(f"Indoklás: {relevancy_result.get('reason')}\n")

if __name__ == "__main__":
    test_question = "Mi a fővárosa Magyarországnak?"
    test_answer = "Budapest Magyarország fővárosa."
    test_context = "Budapest Magyarország legnépesebb városa és fővárosa."

    evaluate_rag(test_question, test_answer, test_context)