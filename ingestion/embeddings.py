from langchain_huggingface import HuggingFaceEmbeddings

def create_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

# --- Test ---
# model = create_embedding_model()
# texte = "La ville d'Antananarivo est la capitale de Madagascar"
# vecteur = model.embed_query(texte)

# print("nombre de dimensions:", len(vecteur))
# print("premieres valeurs:", vecteur[:10])