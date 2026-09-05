from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def create_vector_store(chunks):
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="data/chroma"
    )

    return vector_store