# retriever/embedder.py

import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def load_documents_from_folder(folder_path):
    docs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(folder_path, filename))
            docs.extend(loader.load())
    return docs

def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(docs)

def build_vectorstore(docs, persist_directory="retriever/chroma_db"):
    embeddings = HuggingFaceInferenceAPIEmbeddings(
        api_key=GROQ_API_KEY,
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vectordb.persist()
    print("✅ Vector store created using Groq embeddings and saved to disk.")
    return vectordb

if __name__ == "__main__":
    folder_path = "data"  # Folder containing your PDF laws
    documents = load_documents_from_folder(folder_path)
    print(f"Loaded {len(documents)} documents.")

    chunks = split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")

    db = build_vectorstore(chunks)
