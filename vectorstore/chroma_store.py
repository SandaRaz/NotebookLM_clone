from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from ingestion.embeddings import create_embedding_model

def get_vector_store(embedding_model):
    return Chroma(
        collection_name="documents",
        embedding_function=embedding_model,
        persist_directory="data/chroma"
    )

def create_vector_store(chunks):
    embedding_model = create_embedding_model()
    vector_store = get_vector_store(embedding_model)

    ids = []

    for index, chunk in enumerate(chunks):
        file_hash = chunk.metadata["file_hash"]
        chunk_id = f"{file_hash}_chunk_{index}"
        ids.append(chunk_id)

    # Verifier si les ids existent deja
    existing = vector_store.get(ids=ids)
    existing_ids = set(existing["ids"])

    new_chunks = []
    new_ids = []

    for chunk, chunk_id in zip(chunks, ids):
        if chunk_id not in existing_ids:
            new_chunks.append(chunk)
            new_ids.append(chunk_id)

    if new_chunks:
        vector_store.add_documents(
            documents=new_chunks,
            ids=new_ids
        )

    return vector_store