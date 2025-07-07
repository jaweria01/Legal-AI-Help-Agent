import streamlit as st
from datetime import datetime

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="📘 Urdu Legal Help Assistant",
    layout="wide",
    page_icon="📘",
)

# ----------------- CUSTOM CSS -----------------
st.markdown(r"""
    <style>
        body {
            background-color: #0f172a;
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
    st.image("https://upload.wikimedia.org/wikipedia/commons/3/32/Pakistan_Flag.png", width=120)
    st.markdown('<div class="sidebar-title">📘 Urdu Legal Assistant</div>', unsafe_allow_html=True)
    st.markdown("AI Assistant to understand Pakistani laws in Urdu.")
    st.markdown("---")
    st.markdown('<div class="sidebar-title">📌 Project Info</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="sidebar-section">
    <strong>Created by:</strong> Hassaan's Team<br>
    <strong>Date:</strong> {datetime.today().strftime('%B %d, %Y')}<br>
    <strong>Tech:</strong> Streamlit, Groq, Coral, ChromaDB
    </div>
    """, unsafe_allow_html=True)

# ----------------- HEADER -----------------
st.markdown('<div class="main-title">🧠 Urdu Legal Help Agent 🇵🇰</div>', unsafe_allow_html=True)
st.markdown("A multi-agent assistant to help people understand legal documents in Urdu and English.")
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# ----------------- FILE UPLOAD -----------------
st.subheader("📄 Upload a Legal PDF Document / قانونی دستاویز اپ لوڈ کریں")
uploaded_file = st.file_uploader("Upload a legal Urdu PDF document for analysis / تجزیہ کے لیے اردو قانونی پی ڈی ایف اپ لوڈ کریں:", type=["pdf"])

if uploaded_file:
    st.success("✅ File uploaded successfully / فائل کامیابی سے اپ لوڈ ہو گئی۔")
    if st.button("📤 Start Analysis / تجزیہ شروع کریں"):
        st.info("🔄 Analyzing document with agents (coming soon) / ایجنٹس کے ساتھ دستاویز کا تجزیہ ہو رہا ہے۔")

# ----------------- CHAT ASSISTANT -----------------
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("💬 Ask Questions from Urdu Law / اردو قانون سے سوال پوچھیں")
user_query = st.text_input("Type your legal question in Urdu / اپنا سوال اردو میں درج کریں:")
if user_query:
    st.info(f"🧠 Agent response for: '{user_query}'")
    st.write("(This is where the LLM agent's answer will appear / یہاں AI ایجنٹ کا جواب ظاہر ہوگا)")

# ----------------- SIMPLIFIER -----------------
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("🔎 Simplify Legal Clause / قانونی شق کو آسان بنائیں")
st.text_area("Paste a legal clause (Urdu or English) / اردو یا انگریزی میں قانونی شق درج کریں:")
if st.button("🧾 Simplify it / اسے آسان کریں"):
    st.success("Here is the simplified version (AI-powered coming soon) / آسان کیا گیا متن یہاں ہوگا۔")

# ----------------- DRAFT NOTICE -----------------
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("📬 Draft a Legal Notice / قانونی نوٹس تیار کریں")
st.text_input("Enter recipient name (e.g. Mr. XYZ) / موصول کنندہ کا نام درج کریں:")
st.text_area("Reason for notice (e.g. tenant must vacate) / نوٹس کی وجہ:")
if st.button("📄 Generate Notice / نوٹس تیار کریں"):
    st.success("Your drafted legal notice will appear here / آپ کا تیار کردہ نوٹس یہاں ظاہر ہوگا۔")

# ----------------- RISK HIGHLIGHT -----------------
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("⚠ Highlight Legal Risks / قانونی خطرات کی نشاندہی کریں")
st.text_area("Paste clause to analyze for potential risks / خطرات کے لیے شق درج کریں:")
if st.button("⚠ Analyze Risks / خطرات دیکھیں"):
    st.warning("This is a preview of potential legal risks / ممکنہ قانونی خطرات کی پیشگی معلومات۔")

# ----------------- LAW SUMMARY SECTION -----------------
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("📚 Law Summary Generator / قانون کا خلاصہ بنائیں")
st.text_input("Enter Law Title or Topic / قانون کا عنوان یا موضوع درج کریں:")
if st.button("📘 Summarize Law / خلاصہ تیار کریں"):
    st.success("Here is the summarized version of the law / قانون کا خلاصہ یہاں ظاہر ہوگا۔")

# ----------------- TERM EXPLAINER SECTION -----------------
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("📖 Legal Term Explainer / قانونی اصطلاح کی وضاحت کریں")
st.text_input("Enter legal term (e.g. Khula, Succession) / قانونی اصطلاح درج کریں:")
if st.button("🧾 Explain Term / وضاحت کریں"):
    st.info("This is where the explanation will appear / یہاں اصطلاح کی وضاحت ہوگی۔")