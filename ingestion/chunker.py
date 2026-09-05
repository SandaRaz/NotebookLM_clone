from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents):
    # chunk_size avec pas trop d'informations (recherche moin precis), ni trop petit(contexte insuffisant) 
    # 2 chunks partagent environ 200 characteres
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    return splitter.split_documents(documents)