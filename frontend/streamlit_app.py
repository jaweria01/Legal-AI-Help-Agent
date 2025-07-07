from PyPDF2 import PdfReader
from agents.parse_agent import extract_clauses_from_text
from agents.simplify_agent import simplify_clause
from agents.risk_agent import detect_risks
from agents.draft_agent import generate_notice
import streamlit as st
from datetime import datetime
from openai import OpenAI 


# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Legal AI Help Assistant",
    layout="wide",
    page_icon="📘",
)

# ----------------- CUSTOM CSS -----------------
st.markdown(r"""
    <style>
        body {
            background-color: #0f172a;
        }
        [data-testid="stAppViewContainer"] {
            background-color: #0f172a;
        }
        [data-testid="stHeader"] {
            background-color: #0f172a;
        }
        html , body , [data-testid="stAppViewContainer"] , [data-testid="stHeader"] {
            background-color: #0f172a;
            color: #f1f5f9;
        }
        .highlight-box {
            background-color: #1e293b;
            color: #f1f5f9;
        }
        .stTextInput input ,
        .stTextArea textarea {
            background-color: #1e293b;  
            color: #f1f5f9;
            border: 1px solid #334155;
        }
        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: #cbd5e1;
        }
        .markdown-text-container , .markdown-text-container * {
            color: #f1f5f9;
        }
        label , span , small {
            color: #f1f5f9;
        }
        div[class*="stMarkdown"] p {
            color: #f1f5f9;
        }
        .stButton > button {
            background-color: #facc15;
            color: #0f172a;
        }
        .stAlert {
            background-color: #334155; 
            color: #f8fafc;
        }
        [dat-testid="stMarkdownContainer"] p , 
        .markdown-text-container p ,
        div[class*="stMarkdown"] p 
        section.main p,
        p {
            color: #f1f5f9;
            font-size: 1.05em;
            font-weight: 400;
        }
        .main-title {
            font-size: 2.5em;
            font-weight: bold;
            color: #f8fafc;
            animation: fadeInDown 1s ease-in-out;
        }
        .section-title {
            font-size: 1.5em;
            font-weight: bold;
            color: #facc15;
            margin-top: 1rem;
            animation: fadeInLeft 1s ease-in-out;
        }
        .highlight-box {
            background-color: #1e293b;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            color: #f1f5f9;
            animation: slideUp 0.8s ease-in-out;
        }
        .stButton > button {
            background-color: #facc15 !important;
            color: #0f172a !important;
            border-radius: 8px;
            padding: 0.5rem 1.2rem;
            font-weight: bold;
            transition: all 0.3s ease-in-out;
        }
        .stButton > button:hover {
            background-color: #fde047 !important;
            transform: scale(1.05);
        }
        .section-divider {
            margin: 2rem 0;
            border-top: 2px solid #334155;
        }
        @media screen and (max-width: 768px) {
            .main-title { font-size: 2em; }
            .section-title { font-size: 1.3em; }
            .highlight-box { font-size: 0.95em; }
        }
        [data-testid="stSidebar"] > div:first-child {
            background-color: #0f172a;
            color: #f1f5f9;
            padding: 1.5rem 1rem;
            border-right: 2px solid #334155;
        }
        .sidebar-title {
            font-size: 1.5em;
            font-weight: 700;
            margin-bottom: 1rem;
            color: #facc15;
        }
        .sidebar-section {
            margin-bottom: 1.5rem;
            padding: 0.8rem;
            background-color: #1e293b;
            border-radius: 10px;
            animation: fadeInLeft 1.2s ease-in-out;
        }
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeInLeft {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">📘 Legal AI Help Assistant</div>', unsafe_allow_html=True)
    st.markdown("AI Help Assistant to understand laws.")
    st.markdown("---")
    st.markdown('<div class="sidebar-title">📌 Project Info</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="sidebar-section">
    <strong>Created by:</strong> Team Binary Ninjas<br>
    <strong>Date:</strong> {datetime.today().strftime('%B %d, %Y')}<br>
    <strong>Tech:</strong> Streamlit, Groq, Coral, ChromaDB
    </div>
    """, unsafe_allow_html=True)

# ----------------- HEADER -----------------
st.markdown('<div class="main-title">🧠 Legal AI Help Agent</div>', unsafe_allow_html=True)
st.markdown("A multi-agent assistant to help people understand legal documents in English and Urdu.")
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# ----------------- FILE UPLOAD -----------------
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("📄 Upload a Legal PDF Document (Urdu or English) / قانونی یا انگریزی پی ڈی ایف اپ لوڈ کریں")

uploaded_file = st.file_uploader("Upload a typed PDF (not scanned image):", type=["pdf"])

if uploaded_file:
    st.info("🔄 Extracting text from PDF...")
    pdf_reader = PdfReader(uploaded_file)
    full_text = ""

    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            full_text += page_text + "\n"

    if full_text.strip():
        st.success("✅ Text extracted successfully!")
        
        st.markdown("### 📝 Extracted Text (Editable)")
        full_text = st.text_area("You can modify the extracted content below:", value=full_text, height=300)

        clauses = extract_clauses_from_text(full_text)

        if clauses:
            selected_clause = st.selectbox("📌 Select a Clause to Analyze", clauses)

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("🧠 Simplify Clause"):
                    simplified = simplify_clause(selected_clause)
                    st.markdown("### 📘 Simplified Explanation")
                    st.markdown(simplified)

            with col2:
                if st.button("⚠ Highlight Risk"):
                    risks = detect_risks(selected_clause)
                    st.markdown("### ⚖ Legal Risks Identified")
                    st.markdown(risks)

            with col3:
                if st.button("📩 Draft Notice"):
                    notice = generate_notice(selected_clause)
                    st.markdown("### 📬 Generated Notice")
                    st.markdown(notice)

        else:
            st.warning("⚠ No clear clauses found. Please upload a properly formatted legal document.")
    else:
        st.error("❌ No text extracted. PDF may be a scanned image. Please upload a typed (digital) PDF.")
else:
    st.info("📥 Please upload a PDF file to begin.")

# ----------------- CHAT ASSISTANT -----------------
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("💬 Ask Questions from Urdu Law / اردو قانون سے سوال پوچھیں")
user_query = st.text_input("Type your legal question in Urdu / اپنا سوال اردو میں درج کریں:")
if user_query:
    from openai import OpenAI
    import os
    from dotenv import load_dotenv
    load_dotenv()
    client = OpenAI(base_url=os.getenv("GROQ_BASE_URL"), api_key=os.getenv("GROQ_API_KEY"))
    
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are a Pakistani legal assistant who replies in both English and Urdu."},
            {"role": "user", "content": user_query}
        ]
    )
    st.success(response.choices[0].message.content)

# ----------------- SIMPLIFIER -----------------
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("🔎 Simplify Legal Clause / قانونی شق کو آسان بنائیں")
manual_clause = st.text_area("Paste a legal clause (Urdu or English) / اردو یا انگریزی میں قانونی شق درج کریں:")

if st.button("🧾 Simplify it / اسے آسان کریں") and manual_clause:
    simplified = simplify_clause(manual_clause)
    st.markdown("### 📘 Simplified Explanation / آسان وضاحت")
    st.markdown(simplified)

# ----------------- DRAFT NOTICE -----------------
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("📬 Draft a Legal Notice / قانونی نوٹس تیار کریں")
recipient = st.text_input("Enter recipient name (e.g. Mr. XYZ) / موصول کنندہ کا نام درج کریں:")
reason_clause = st.text_area("Reason for notice (e.g. tenant must vacate) / نوٹس کی وجہ:")

if st.button("📄 Generate Notice / نوٹس تیار کریں") and reason_clause:
    notice_text = generate_notice(reason_clause, recipient)
    st.markdown("### 📨 Generated Legal Notice / تیار کردہ قانونی نوٹس")
    st.markdown(notice_text)

# ----------------- RISK HIGHLIGHT -----------------
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("⚠ Highlight Legal Risks / قانونی خطرات کی نشاندہی کریں")
risk_clause = st.text_area("Paste clause to analyze for potential risks / خطرات کے لیے شق درج کریں:")

if st.button("⚠ Analyze Risks / خطرات دیکھیں") and risk_clause:
    risks = detect_risks(risk_clause)
    st.markdown("### ⚖ Detected Legal Risks / دریافت شدہ قانونی خطرات")
    st.markdown(risks)

# ----------------- LAW SUMMARY SECTION -----------------
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("📚 Law Summary Generator / قانون کا خلاصہ بنائیں")
st.text_input("Enter Law Title or Topic / قانون کا عنوان یا موضوع درج کریں:")
if st.button("📘 Summarize Law / خلاصہ تیار کریں") and summ_topic:
    summary_prompt = f"Summarize the Pakistani law or topic: {summ_topic} in plain Urdu and English."
    summary_response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": summary_prompt}]
    )
    st.success(summary_response.choices[0].message.content)

# ----------------- TERM EXPLAINER SECTION -----------------
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("📖 Legal Term Explainer / قانونی اصطلاح کی وضاحت کریں")
st.text_input("Enter legal term (e.g. Khula, Succession) / قانونی اصطلاح درج کریں:")
if st.button("🧾 Explain Term / وضاحت کریں") and term:
    term_prompt = f"Explain the legal term '{term}' in Urdu and English with an example."
    term_response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": term_prompt}]
    )
    st.success(term_response.choices[0].message.content)