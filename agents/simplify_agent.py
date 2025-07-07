# agents/simplify_agent.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load GROQ credentials
load_dotenv()

# Initialize client using Groq-compatible OpenAI library
client = OpenAI(
    base_url=os.getenv("GROQ_BASE_URL"),
    api_key=os.getenv("GROQ_API_KEY")
)

# Main function: takes a clause and returns explanation
def simplify_clause(clause_text):
    prompt = f"""
آپ ایک ماہر قانونی معاون ہیں جو اردو اور انگریزی میں قانونی شقوں کی سادہ زبان میں وضاحت کرتا ہے۔

Clause:
{clause_text}

براہ کرم درج ذیل فارمیٹ میں وضاحت دیں:

1. ✅ سادہ اردو میں وضاحت
2. ✅ Plain English explanation
    """

    # Send to Groq LLaMA3
    response = client.chat.completions.create(
        model="llama3-70b-8192",  # Required model for Raise Hackathon
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    return response.choices[0].message.content


# If you want to test it standalone:
if _name_ == "_main_":
    clause = "شق 3: مالک مکان کرایہ دار کو کم از کم 30 دن پہلے تحریری نوٹس دے گا۔"
    print(simplify_clause(clause))