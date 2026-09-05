from langchain_ollama import ChatOllama
from .prompt import create_rag_prompt

MODEL_NAME = "Qwen"

def create_llm():
    return ChatOllama(
        model="qwen2.5:1.5b",
        temperature=0
    )

def generate_answer(question, documents):
    llm = create_llm()
    prompt = create_rag_prompt()

    context = "\n\n".join(
        document.page_content for document in documents
    )

    prompt_text = prompt.format(
        context=context,
        question=question
    )

    response = llm.invoke(prompt_text)

    return response.content


# --- Test ---
# from retrieval.search import search_documents

# question = "Qu'est-ce que le Deep Learning ?"
# documents = search_documents(question, k=5)
# reponse = generate_answer(
#     question,
#     documents
# )

# print("\nRéponse de Qwen :")
# print(reponse)