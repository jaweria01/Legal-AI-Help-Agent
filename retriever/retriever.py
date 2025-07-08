import os
import glob
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

load_dotenv()

# ✅ Embedding model: Groq-compatible OpenAIEmbeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small",  # Optional: you can change to ada-002
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

CHROMA_DIR = "chroma_db"

def create_vector_store():
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200
    )
    documents = []

    # Load all .txt files from /data/
    for file_path in glob.glob("data/*.txt"):
        loader = TextLoader(file_path, encoding="utf-8")
        docs = loader.load_and_split(text_splitter)
        documents.extend(docs)

    # Store embeddings in ChromaDB
    db = Chroma.from_documents(
        documents,
        embedding=embedding_model,
        persist_directory=CHROMA_DIR
    )
    db.persist()
    print("✅ Vector store created and saved to", CHROMA_DIR)

def search_similar_documents(query, top_k=3):
    db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embedding_model)

    try:
        query_embedding = embedding_model.embed_query(query)
        results = db.similarity_search_with_score_by_vector(query_embedding, k=top_k)

        chunks = [doc.page_content for doc, _ in results]
        sources = [doc.metadata.get("source", "N/A") for doc, _ in results]

        return chunks, sources

    except Exception as e:
        print(f"❌ Error during retrieval: {e}")
        return [], []

if __name__ == "__main__":
    create_vector_store()
