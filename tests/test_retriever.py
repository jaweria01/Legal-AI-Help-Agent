# test_retriever.py placeholder

from retriever.retriever import search_similar_documents

def test_retriever_returns_law_chunks():
    query = "وراثت میں بیٹی کا حصہ"
    chunks, sources = search_similar_documents(query)

    assert isinstance(chunks, list), "❌ Chunks should be a list"
    assert len(chunks) > 0, "❌ No results returned from retriever"
    print("✅ Retriever test passed: chunks returned for query.")
