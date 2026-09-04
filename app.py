import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="NotebookLM Clone",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Chargement bootstrap local
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

# Etat de l'application
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

    st.markdown("### Sources")

    fichiers = st.file_uploader(
        "Ajouter des documents",
        type=["pdf", "md", "txt"],
        accept_multiple_files=True
    )

    if fichiers:
        st.caption(f"{len(fichiers)} document(s) selectionné(s)")

        for fichier in fichiers:
            st.markdown(
                f"📄 {fichier.name}"
            )

    st.markdown("")

    if st.button(
        "Indexer les docs",
        use_container_width=True
    ):
        if fichiers:
            st.success("Documents prets pour l'indexation")
        else:
            st.warning("Ajouter d'abord un document")

    st.divider()

    st.markdown("### Modele")

    st.session_state.rag_mode = st.toggle(
        "Assistant RAG",
        value=st.session_state.rag_mode
    )

    if st.session_state.rag_mode:
        st.caption("🟢 Assistant RAG complet")
    else:
        st.caption("🔴 Recherche semantique pure")

# --- END SIDEBAR ---

# ===== ZONE PRINCIPALE =====

st.markdown(
    """
    <div class="mb-4">
        <div class="app-title">Assistant documentaire</div>
        <div class="app-subtitle">
            Posez une question a propos de vos documents.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -- Historiques --
if not st.session_state.messages:
    st.markdown(
        """
        <div class="chat-card text-center">
            <div style="font-size: 2rem;"></div>
            <h5>Bienvenue</h5>
            <p class="text-muted mb-0">
                Importez vos documents puis posez une question.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )     
else: 
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])  

# -- Input Converstion --
question = st.chat_input("Posez une question...")

if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    if not st.session_state.llm_active:
        reponse = "Le RAG LLM est actuellement desactivé"
    else:
        reponse = (
            "Le système RAG n'est pas encore connecté. "
            "Cette partie sera ajoutée dans les prochaines étapes."
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reponse
        }
    )

    with st.chat_message("assistant"):
        st.markdown(reponse)

# === END ZONE PRINCIPALE ===
