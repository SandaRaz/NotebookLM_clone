from pathlib import Path
import tempfile
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    TextLoader
)

def extract_file(file_path: str):
    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        loader = PyMuPDFLoader(file_path)
    elif extension in [".txt", ".md"]:
        loader = TextLoader(
            file_path,
            encoding="utf-8"
        )
    else:
        raise ValueError(f"Format non supporté: {extension}")

    # Retourne un Document LangChain
    return loader.load()

# Depuis des objets de type UploadedFile
def extract_from_uploaded_files(fichiers):
    documents = []

    for fichier in fichiers:
        suffix = Path(fichier.name).suffix

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:
            temp_file.write(fichier.getvalue())
            temp_path = temp_file.name

        docs = extract_file(temp_path)

        for doc in docs:
            doc.metadata["source"] = fichier.name

        documents.extend(docs)

        # --- Test ---
        for doc in docs:
            print(f"Name: {fichier.name}")
            print(f"    Metadata source: {doc.metadata}")
            print(f"    Content: \n {doc.page_content[:1000]}")

    return documents