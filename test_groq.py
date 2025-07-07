import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env key
load_dotenv()

client = OpenAI(
    base_url=os.getenv("GROQ_BASE_URL"),
    api_key=os.getenv("GROQ_API_KEY")
)

response = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {"role": "user", "content": "قانون کی یہ شق کیا کہتی ہے: کرایہ دار کو 30 دن میں مکان خالی کرنا ہوگا؟"}
    ],
    temperature=0.5,
)

print(response.choices[0].message.content)