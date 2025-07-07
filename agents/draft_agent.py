# agents/draft_agent.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Setup Groq client
client = OpenAI(
    base_url=os.getenv("GROQ_BASE_URL"),
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_notice(clause_text, recipient="Tenant"):
    prompt = f"""
You are a legal assistant that helps draft formal legal notices in both English and Urdu.

Based on the clause below, generate a short, polite, but legally valid notice letter for the recipient.

Clause:
{clause_text}

Recipient: {recipient}

Output:
1. 📄 English Legal Notice  
2. 📄 اردو قانونی نوٹس (سادہ اور رسمی زبان میں)
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    return response.choices[0].message.content


# Optional test run
if _name_ == "_main_":
    clause = "شق 7: کرایہ دار کو 30 دن کے اندر مکان خالی کرنا ہوگا ورنہ قانونی کارروائی ہو سکتی ہے۔"
    print(generate_notice(clause, recipient="کرایہ دار"))