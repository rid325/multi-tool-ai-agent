"""
Memory — persists conversation history to memory.json.
Allows the agent to reference previous interactions.
"""
import json
import logging
import pathlib
from datetime import datetime

logger = logging.getLogger(__name__)
MEMORY_FILE = pathlib.Path("memory.json")


def _load() -> list[dict]:
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text())
        except Exception:
            pass
    return []


def _save(history: list[dict]):
    try:
        MEMORY_FILE.write_text(json.dumps(history, indent=2))
    except Exception as e:
        logger.warning("Could not save memory: %s", e)


def append(role: str, content: str):
    history = _load()
    history.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat(),
    })
    _save(history)
    logger.debug("Memory updated — %d entries", len(history))


def get_recent(n: int = 6) -> list[dict]:
    """Return last n exchanges as role/content dicts (no timestamp) for LLM context."""
    history = _load()
    recent = history[-n:]
    return [{"role": h["role"], "content": h["content"]} for h in recent]


def get_summary() -> str:
    history = _load()
    if not history:
        return ""
    lines = [f"- [{h['role']}]: {h['content'][:80]}" for h in history[-4:]]
    return "Recent conversation:\n" + "\n".join(lines)


def clear():
    _save([])
    logger.info("Memory cleared.")
