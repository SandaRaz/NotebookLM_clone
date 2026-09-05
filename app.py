import streamlit as st
from pathlib import Path
from ingestion.extractors import extract_from_uploaded_files
from ingestion.chunker import split_documents
from vectorstore.chroma_store import create_vector_store
from retrieval.search import search_documents
from generation.llm import MODEL_NAME, generate_answer
from history.manager import (
    create_conversation,
    save_conversation,
    load_conversation,
    list_conversations
)

# --- Configuration ---

st.set_page_config(
    page_title="NotebookLM Clone",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Chargement bootstrap local ---
bootstrap_css = Path("static/css/bootstrap.min.css").read_text(encoding="utf-8")
bootstrap_js = Path("static/js/bootstrap.bundle.min.js").read_text(encoding="utf-8")

st.markdown(
    f"<style>{bootstrap_css}</style>",
    unsafe_allow_html=True
)

# --- CSS ZONE ---

st.markdown(
    """
    <style>

        /* Fond général */
        .stApp {
            background-color: #f8f9fa;
        }

        /* Réduire l'espace supérieur */
        .block-container {
            padding-top: 2rem;
        }

        /* Titre */
        .app-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 0;
        }

        .app-subtitle {
            color: #6c757d;
            font-size: 0.9rem;
        }

        /* Carte */
        .chat-card {
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
        }

        .chat-role {
            font-weight: 600;
            margin-bottom: 0.4rem;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: white;
        }

    </style>
    """,
    unsafe_allow_html=True
)

# - END CSS ZONE -

# --- Initiation de la session ---
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = create_conversation()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_mode" not in st.session_state:
    st.session_state.rag_mode = True



# ----- SIDEBAR -----

with st.sidebar:
    st.markdown(
        """
        <div class="mb-4">
            <h2>NotebookLM Clone</h2>
            <p class="text-muted">
                Assistant documentaire local
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ----- SOURCES -----

    st.markdown("### Sources")

    fichiers = st.file_uploader(
        "Ajouter des documents",
        type=["pdf", "md", "txt"],
        accept_multiple_files=True
    )

    if fichiers:
        st.caption(f"{len(fichiers)} document(s) selectionné(s)")

        for fichier in fichiers:
            st.markdown(f"📄 {fichier.name}")

    st.markdown("")

    if st.button(
        "Indexer les documents",
        use_container_width=True
    ):
        if not fichiers:
            st.warning("Ajouter d'abord un document")
        else:
            with st.spinner("Indexation en cours..."):
                documents = extract_from_uploaded_files(fichiers)

                chunks = split_documents(documents)
                # --- Test ---
                # for i, chunk in enumerate(chunks):
                #     print(f"\n {i + 1}: {len(chunk.page_content)} caracteres")

                create_vector_store(chunks)

                # resultats = vector_store.get()
                # st.write("Nombre de chunks dans Chroma :", len(resultats["documents"]))

                print(f"{len(documents)} document(s) extrait(s) -> {len(chunks)} chunk(s)")
                st.success("Document(s) indexé(s)")   

    st.divider()

    # --- END SOURCES ---

    # ----- MODE -----

    st.markdown("### Modele")

    st.session_state.rag_mode = st.toggle(
        "RAG activé",
        value=st.session_state.rag_mode
    )

    if st.session_state.rag_mode:
        st.caption("🟢 RAG complet")
    else:
        st.caption("🔴 Recherche semantique")

    st.divider()

    # --- END MODE ---

    # ----- HISTORIQUE -----

    st.markdown("### Historique")

    if st.button(
        "Nouvelle conversation",
        use_container_width=True
    ):
        st.session_state.conversation_id = (
            create_conversation()
        )
        st.session_state.messages = []
        st.rerun()

    conversations = list_conversations()

    for conversation_file in conversations:
        conversation_id = conversation_file.stem

        if conversation_id == st.session_state.conversation_id:
            label = f"🟢 {conversation_id}"
        else:
            label = conversation_id

        if st.button(
            label,
            key=f"conversation_{conversation_id}",
            use_container_width=True
        ):
            st.session_state.conversation_id = (
                conversation_id
            )

            st.session_state.messages = (
                load_conversation(conversation_id)
            )

            st.rerun()

    # --- END HISTORIQUE ---

# --- END SIDEBAR ---


# ======= ZONE PRINCIPALE =======

# ----- EN-TETE -----

st.markdown(
    """
    <div class="mb-4">
        <div class="app-title">
            Assistant documentaire
        </div>
        <div class="app-subtitle">
            Posez une question à propos de vos documents.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- END EN-TETE ---

# ----- HISTORIQUE DE LA CONVERSATION ACTUELLE -----

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(
            message["content"]
        )

        # Affichage des sources sauvegardees
        if message.get("sources"):
            with st.expander("Voir les extraits utilisés"):
                for i, source in enumerate(message["sources"],start=1):
                    st.markdown(
                        f"**Extrait {i} — {source['filename']}**"
                    )

                    st.write(
                        source["content"]
                    )

                    st.divider()

# -------------------------------------------------- 

# --- Input Conversation ---
question = st.chat_input("Posez une question...")

if question:
    user_message = {
        "role": "user",
        "content": question
    }

    st.session_state.messages.append(user_message)

    with st.chat_message("user"):
        st.markdown(question)

    # -- Recherche des chunks --
    with st.spinner("Recherche dans les documents..."):
        documents = search_documents(question,k=5)

    # Preparation des sources pour historique
    sources = []

    for document in documents:
        sources.append(
            {
                "filename": document.metadata.get(
                    "source",
                    "Source inconnue"
                ),
                "content": document.page_content
            }
        )

    # Si recherche semantique et non rag
    if not st.session_state.rag_mode:
        with st.chat_message("assistant"):
            st.markdown("### Résultats de la recherche sémantique")

            for i, document in enumerate(documents, start=1):
                source = document.metadata.get("source", "Source inconnue")

                st.markdown(f"**Résultat {i} — {source}**")
                st.write(document.page_content)
                st.divider()

        assistant_message = {
            "role": "assistant",
            "content": (
                "Résultats de la recherche sémantique"
            ),
            "sources": sources
        }

    # Mode rag complet
    else:
        with st.spinner(f"{MODEL_NAME} analyse les documents..."):
            reponse = generate_answer(question, documents)

        with st.chat_message("assistant"):
            st.markdown(reponse)

            # -- Transparence --
            with st.expander("Voir les extraits utilisés comme contexte"):
                for i, source in enumerate(sources, start=1):
                    st.markdown(f"**Extrait {i} — {source['filename']}**")
                    st.write(source["content"])

                    st.divider()

        assistant_message = {
            "role": "assistant",
            "content": reponse,
            "sources": sources
        }

    st.session_state.messages.append(
        assistant_message
    )

    # -- Sauvegarde JSON --
    save_conversation(
        st.session_state.conversation_id,
        st.session_state.messages
    )

# ===== END ZONE PRINCIPALE =====
