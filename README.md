# 🧠 Legal E-commerce AI Agent
An agentic Urdu+English AI system to help users — especially in Pakistan — understand legal documents, simplify complex clauses, highlight risks, and draft notices.

Built for the [RAISE Your Hack 2025](https://lablab.ai) Hackathon — submitted under the Prosus Track.

---

## 🔍 Problem  
Millions in Pakistan and other Urdu-speaking countries struggle to understand legal documents due to:

- Complex language (English, legalese)  
- Lack of regional language support  
- Expensive legal consultations  
- No access to AI tools for local laws

---

## 💡 Solution: Legal E-commerce AI Agent 
We built a multi-agent AI system powered by Groq & LangChain that:

✅ Extracts important clauses from legal Urdu PDFs  
✅ Explains them in plain Urdu + English  
✅ Highlights risks in contracts  
✅ Drafts legal notices automatically  
✅ Lets you ask legal questions in Urdu  
✅ Supports 50+ Pakistani federal laws

---

## 🛠️ Tech Stack

| Layer         | Tools Used                                      |
|---------------|--------------------------------------------------|
| 💻 Frontend    | Streamlit (responsive, Urdu+English dual UI)    |
| 🧠 LLM         | LLaMA-3 via Groq API and Groq                          |
| 🧱 Agents       | Coral Protocol + LangChain + Multi-Agent Architecture            |
| 📄 Data        |  Federal Laws in PDF (Urdu + English)        |
| 🔎 Retrieval   | ChromaDB + Groq Embedding Model                 |
| 🔐 Secrets     | .env via python-dotenv                          |

---

## 🗂️ Folder Structure

/legal-ecom-agent
├── agents/
│ ├── simplify_agent.py
│ ├── draft_agent.py
│ ├── risk_agent.py
│ └── user_profile.py
├── retriever/
│ ├── embedder.py
│ └── retriever.py
├── frontend/
│ └── streamlit_app.py
├── data/ ← Cleaned Urdu law texts
├── tests/ ← test_agents.py, test_retriever.py
├── .env ← Stores GROQ_API_KEY
├── requirements.txt
├── README.md


---

## ⚙️ How to Run Locally

1. Clone this repo  

2. Create a .env file:

3. Install dependencies:

4. Embed the data:

5. Run the app:

---

## ✨ Features (Demo-Ready)

- 🧠 Ask legal questions → gets answer from PDF or LLM  
- 📄 Upload PDF → extracts + simplifies clauses  
- 📝 Draft Notice → name + reason → AI generates legal Urdu letter  
- ⚠ Risk Detection → clause → AI flags dangerous parts  
- 📘 Law Summary → type law name → summary  
- 📖 Term Explainer → define Urdu legal terms (e.g. خلع, وراثت)

---

## 📚 Sample Laws Included

- دستور پاکستان 1973  
- قانون شہادت 1984  
- تعزیرات پاکستان  
- انسداد دہشتگردی  
- قانونِ وراثت، نکاح، خلع، اجرت، اور مزید 50+ اردو قوانین

---

## 👥 Team: Binary Ninjas

- Muhammad Hassaan — Team Leader / Full Stack developer
- Jaweria Siddique — Data Engineer
- Muhammad Haris — Retriever Specialist
- Qutaiba Ansari — LLM Agent Engineer
- Gohar Fatima - Frontend developer
- Saman Fatima— Pitch & Testing

---

## 📦 Deployment

- Groq API: https://console.groq.com  
- Streamlit App: Local or Hugging Face (optional)  
- Hugging Face Demo UI (optional): [add link]

---

## 📌 License

MIT License — for educational and nonprofit use.

---

## 🚀 Bonus Features (if implemented)

- PDF Export of results  
- Urdu/English chat assistant with memory  
- Saving user profiles as Knowledge Graphs

---

👨‍⚖️ Built by Binary Ninjas for Pakistan 🇵🇰 and all communities needing legal clarity.
