# agents/risk_agent.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Initialize Groq LLM client
client = OpenAI(
    base_url=os.getenv("GROQ_BASE_URL"),
    api_key=os.getenv("GROQ_API_KEY")
)

def detect_risks(clause_text):
    prompt = f"""
You are a legal assistant and compliance risk advisor.

Your task is to carefully review the following legal clause and identify any possible legal risks, ambiguities, or problematic conditions.

Clause:
{clause_text}

Respond in this format:

1. ⚠ Risk(s) or ambiguity in English  
2. ⚠ اردو میں قانونی خطرے کی مختصر وضاحت  
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    return response.choices[0].message.content


# Run standalone for testing
if __name__ == "__main__":
    clause = "شق 5: مالک مکان کرایہ بغیر اطلاع کے کسی بھی وقت بڑھا سکتا ہے۔"
    print(detect_risks(clause))