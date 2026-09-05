from langchain_core.prompts import PromptTemplate

# Creer un template de prompt pour un system strict
def create_rag_prompt():
    return PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a document assistant.

Answer the user's question using ONLY the information
contained in the provided context.

Strict rules:
- Do not use any knowledge outside the provided context.
- If the answer cannot be found in the context, say: "I cannot find the answer in the provided documents."
- Do not invent or assume information that is not present in the context.
- Answer in the same language as the user's question.
- Be clear and concise.

Context:
{context}

Question:
{question}

Answer:
"""
    )

# --- Test ---
# prompt = create_rag_prompt()

# texte = prompt.format(
#     context="Le Deep Learning apprend des représentations hiérarchiques.",
#     question="Qu'est-ce que le Deep Learning ?"
# )

# print(texte)