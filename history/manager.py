import json
from pathlib import Path
from datetime import datetime

CONVERSATIONS_DIR = Path("data/conversations")

def create_conversation():
    CONVERSATIONS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )
    conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    return conversation_id

def save_conversation(conversation_id, messages):
    CONVERSATIONS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = CONVERSATIONS_DIR / f"{conversation_id}.json"

    with open(file_path,"w",encoding="utf-8") as file:
        json.dump(
            {
                "id": conversation_id,
                "messages": messages
            },
            file,
            ensure_ascii=False,
            indent=2
        )

def load_conversation(conversation_id):
    file_path = CONVERSATIONS_DIR / f"{conversation_id}.json"

    if not file_path.exists():
        return []

    with open(file_path,"r",encoding="utf-8") as file:
        data = json.load(file)

    return data.get("messages", [])

def list_conversations():
    CONVERSATIONS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    return sorted(
        CONVERSATIONS_DIR.glob("*.json"),
        reverse=True
    )