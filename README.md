# NotebookLM Clone
Systeme reposant sur l'architecture **RAG** (Retrieval-Augmented Generation) local

---

## Prérequis:

* **Python 3.10+**.
* **[Ollama](https://ollama.com/)** installé et exécuté en arrière-plan.
* Un modèle LLM téléchargé et fonctionnel via Ollama (ex. `qwen2.5:1.5b`, `llama3.2`, ou `mistral`).

Pour lancer un modèle localement via Ollama :
```bash
ollama run qwen2.5:1.5b
```

## Installation:
Créer et activer l'environnement virtuel

* Sur Linux / macOS :
```bash
python3 -m venv venv
source venv/bin/activate
```

* Sur Windows (PowerShell) :
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

* Installer les dépendances:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

* Modifiez le fichier ingestion/embeddings.py pour changer le modèle d'embedding Hugging Face utilisé pour la vectorisation
* Modifiez le fichier generation/llm.py pour changer le modèle Ollama exécuté par le système

**Notice :**
Lors du tout premier lancement, l'application peut prendre plusieurs minutes (le système télécharge localement le modèle d'embeddings)