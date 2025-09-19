import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.simplify_agent import simplify_clause
from agents.risk_agent import detect_risks
from agents.draft_agent import generate_notice
from agents.parse_agent import extract_clauses_from_text
from PyPDF2 import PdfReader
from retriever.retriever import search_similar_documents
import streamlit as st
from datetime import datetime
from openai import OpenAI 
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url=os.getenv("GROQ_BASE_URL")
)

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Legal AI Help Agent",
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
        div.stButton > button, div.row-widget.stButton > button, button[kind="formSubmit"] {
            background-color: #facc15 !important;   /* yellow */
            color: #0f172a !important;              /* dark navy text */
            border: none;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.5rem 1.2rem;
            transition: all 0.3s ease-in-out;
        }
        div.stButton > button:hover, 
        div.row-widget.stButton > button:hover, 
        button[kind="formSubmit"]:hover {
            background-color: #fde047 !important;   /* hover lighter yellow */
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
    <strong>Tech:</strong> Streamlit, Groq, LLaMA, LangChain, ChromaDB and more.
    </div>
    """, unsafe_allow_html=True)

# ----------------- HEADER -----------------
st.markdown('<div class="main-title">🧠 Legal AI Help Agent</div>', unsafe_allow_html=True)
st.markdown("A multi-agent assistant to help people understand legal documents in English and Urdu.")
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# ----------------- FILE UPLOAD -----------------
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("📄 Upload a Legal PDF Document (English or Urdu) / قانونی پی ڈی ایف دستاویز اپ لوڈ کریں (انگریزی یا اردو)")

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

# ----------------- ASK QUESTION SECTION -----------------
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("💬 Ask Questions related to the Law / قانون سے متعلق سوالات پوچھیں۔")

user_query = st.text_input("Type your legal question /  اپنا قانونی سوال درج کریں :")

# Initialize session state for response
if "question_response" not in st.session_state:
    st.session_state.question_response = ""

# Handle button click
if st.button("🔍 Get Answer / جواب حاصل کریں"):
    if user_query.strip():
        chunks, sources = search_similar_documents(user_query)

        if chunks:
            context = "\n\n".join(chunks)
            prompt = f"""Context:\n{context}\n\nQuestion:\n{user_query}\n\nAnswer this legal question in both Urdu and English:"""
        else:
            prompt = f"Answer this legal question in both Urdu and English: {user_query}"

        try:
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            st.session_state.question_response = response.choices[0].message.content.strip()

        except Exception as e:
            st.session_state.question_response = f"❌ Error: {str(e)}"

# Show response
if st.session_state.question_response:
    st.markdown("🧠 Agent Response / ایجنٹ کا جواب:")
    st.success(st.session_state.question_response)


# ----------------- SIMPLIFIER -----------------
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("🔎 Simplify Legal Clause / قانونی شق کو آسان بنائیں")

clause_text = st.text_area("Paste a legal clause (English or Urdu) / انگریزی یا اردو میں قانونی شق درج کریں:")

# Initialize session state
if "simplified_output" not in st.session_state:
    st.session_state.simplified_output = ""

if st.button("🧾 Simplify it / اسے آسان کریں"):
    if clause_text.strip():
        chunks, sources = search_similar_documents(clause_text)

        if chunks:
            context = "\n\n".join(chunks)
            prompt = f"""Context:\n{context}\n\nClause:\n{clause_text}\n\nSimplify this clause in both Urdu and English:"""
        else:
            prompt = f"Simplify this legal clause (in Urdu and English): {clause_text}"

        try:
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.simplified_output = response.choices[0].message.content.strip()

        except Exception as e:
            st.session_state.simplified_output = f"❌ Error: {str(e)}"

# Show response
if st.session_state.simplified_output:
    st.markdown("🧾 Simplified Clause / آسان شدہ شق:")
    st.success(st.session_state.simplified_output)


# ----------------- DRAFT NOTICE -----------------
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("📬 Draft a Legal Notice / قانونی نوٹس تیار کریں")

recipient = st.text_input("Enter recipient name (e.g. Mr. XYZ) / موصول کنندہ کا نام درج کریں:")
notice_reason = st.text_area("Reason for notice (e.g. tenant must vacate) / نوٹس کی وجہ:")

# Initialize session state
if "drafted_notice_output" not in st.session_state:
    st.session_state.drafted_notice_output = ""

if st.button("📄 Generate Notice / نوٹس تیار کریں"):
    if recipient.strip() and notice_reason.strip():
        chunks, sources = search_similar_documents(notice_reason)

        if chunks:
            context = "\n\n".join(chunks)
            prompt = f"""Context:\n{context}\n\nDraft a formal legal notice in both Urdu and English based on the following reason:\n"{notice_reason}"\nAddressed to: {recipient}"""
        else:
            prompt = f"""Draft a formal legal notice in both Urdu and English with the following reason:\n"{notice_reason}"\nAddressed to: {recipient}"""

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.drafted_notice_output = response.choices[0].message.content.strip()

        except Exception as e:
            st.session_state.drafted_notice_output = f"❌ Error: {str(e)}"

# Show output
if st.session_state.drafted_notice_output:
    st.markdown("📬 Drafted Notice / تیار کردہ نوٹس:")
    st.success(st.session_state.drafted_notice_output)

# ----------------- RISK HIGHLIGHT -----------------
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("⚠ Highlight Legal Risks / قانونی خطرات کی نشاندہی کریں")

risk_clause = st.text_area("Paste clause to analyze for potential risks / خطرات کے لیے شق درج کریں:")

# Initialize session state
if "risk_output" not in st.session_state:
    st.session_state.risk_output = ""

if st.button("⚠ Analyze Risks / خطرات دیکھیں"):
    if risk_clause.strip():
        chunks, sources = search_similar_documents(risk_clause)

        if chunks:
            context = "\n\n".join(chunks)
            prompt = f"""Context:\n{context}\n\nClause:\n{risk_clause}\n\nIdentify any legal risks, unclear language, or missing terms in this clause. Explain in Urdu and English."""
        else:
            prompt = f"Identify any legal risks, unclear language, or missing terms in this clause. Explain in Urdu and English:\n\n{risk_clause}"

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.risk_output = response.choices[0].message.content.strip()

        except Exception as e:
            st.session_state.risk_output = f"❌ Error: {str(e)}"

# Display output
if st.session_state.risk_output:
    st.markdown("⚠️ Legal Risk Analysis / قانونی خطرات:")
    st.warning(st.session_state.risk_output)

# ----------------- LAW SUMMARY SECTION -----------------
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("📚 Law Summary Generator / قانون کا خلاصہ بنائیں")

summ_topic = st.text_input("Enter Law Title or Topic / قانون کا عنوان یا موضوع درج کریں:")

# Initialize session state
if "law_summary_output" not in st.session_state:
    st.session_state.law_summary_output = ""

if st.button("📘 Summarize Law / خلاصہ تیار کریں"):
    if summ_topic.strip():
        chunks, sources = search_similar_documents(summ_topic)

        if chunks:
            context = "\n\n".join(chunks)
            prompt = f"""Context:\n{context}\n\nSummarize the above law or topic in both Urdu and English for better understanding."""
        else:
            prompt = f"""Summarize the Pakistani law or topic: {summ_topic} in both Urdu and English."""

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.law_summary_output = response.choices[0].message.content.strip()

        except Exception as e:
            st.session_state.law_summary_output = f"❌ Error: {str(e)}"

# Show output
if st.session_state.law_summary_output:
    st.markdown("📘 Summary Output / خلاصہ:")
    st.success(st.session_state.law_summary_output)

# ----------------- TERM EXPLAINER SECTION -----------------
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("📖 Legal Term Explainer / قانونی اصطلاح کی وضاحت کریں")

term = st.text_input("Enter legal term (e.g. Khula, Succession) / قانونی اصطلاح درج کریں:")

# Initialize session state
if "term_explainer_output" not in st.session_state:
    st.session_state.term_explainer_output = ""

if st.button("🧾 Explain Term / وضاحت کریں"):
    if term.strip():
        chunks, sources = search_similar_documents(term)

        if chunks:
            context = "\n\n".join(chunks)
            prompt = f"""Context:\n{context}\n\nExplain the term "{term}" in both Urdu and English for general public understanding."""
        else:
            prompt = f"""Explain the legal term "{term}" in both Urdu and English so a non-lawyer can understand it easily."""

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.term_explainer_output = response.choices[0].message.content.strip()

        except Exception as e:
            st.session_state.term_explainer_output = f"❌ Error: {str(e)}"

# Show output
if st.session_state.term_explainer_output:
    st.markdown("🧾 Explanation Output / وضاحت:")
    st.success(st.session_state.term_explainer_output)

