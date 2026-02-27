import json
import hashlib
from datetime import datetime
from pathlib import Path

LOG_PATH = Path.home() / "tucker_console" / "logs" / "audit.jsonl"

def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def log_event(intent, prompt, status, model, user_id="anonymous", safety_flags=None, notes=""):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_id": user_id,
        "intent": intent,
        "prompt_hash": _hash(prompt),
        "status": status,
        "model": model,
        "safety_flags": safety_flags or [],
        "notes": notes,
    }
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
