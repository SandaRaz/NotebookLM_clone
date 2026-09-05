from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from ingestion.embeddings import create_embedding_model
from vectorstore.chroma_store import get_vector_store

def search_documents(question, k=5):
    embedding_model = create_embedding_model();
    vector_store = get_vector_store(embedding_model)

    return vector_store.similarity_search(question, k=k)