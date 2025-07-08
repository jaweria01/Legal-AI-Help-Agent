# agents/parse_agent.py

import re
from retriever.retriever import embed_query, search_similar_chunks
from agents.user_profile import save_user_query

def extract_clauses_from_text(text):
    # ... your existing splitting logic ...
    return clauses

def handle_user_question(user_input):
    # NEW: Full agent pipeline
    embedding = embed_query(user_input)
    best_chunks = search_similar_chunks(embedding)

    best_clause = best_chunks[0] if best_chunks else "❌ کوئی متعلقہ شق نہیں ملی۔"

    simplified = best_clause
    risk = None
    notice = None

    save_user_query(
        user_id="user123",
        clause=best_clause,
        explanation=simplified,
        risk=risk,
        notice=notice
    )

    return best_clause

if __name__ == "__main__":
    # ✅ Test the pipeline
    answer = handle_user_question("کرایہ داری قانون دفعہ پانچ کیا ہے؟")
    print("🧠 Agent Response:", answer)
