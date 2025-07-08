# test_agents.py placeholder

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def test_simplify_agent_llm_response():
    clause = "کرایہ دار کو 30 دن پہلے نوٹس دینا ہوگا"
    prompt = f"Simplify this clause in Urdu and English: {clause}"

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response.choices[0].message.content
    assert answer.strip() != "", "❌ Empty response from simplify agent"
    print("✅ Simplify agent test passed")

def test_notice_drafting_llm_response():
    recipient = "Mr. Khan"
    reason = "Tenant refuses to vacate"
    prompt = f"Draft a legal notice in Urdu and English for {recipient} due to: {reason}"

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response.choices[0].message.content
    assert "محترم" in answer or "Dear" in answer, "❌ Notice draft did not contain proper greeting"
    print("✅ Notice agent test passed")
