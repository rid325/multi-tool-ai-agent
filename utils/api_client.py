"""
API Client — wraps Google Gemini chat completions using google-genai SDK.
Requires GEMINI_API_KEY in .env
"""
import os
import logging

logger = logging.getLogger(__name__)


def chat_completion(messages: list[dict], model: str | None = None) -> str:
    """Send messages to Gemini and return the assistant reply as a string."""
    resolved_model = model or _load_config_model() or "gemini-2.0-flash"

    try:
        from google import genai  # type: ignore
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError("GEMINI_API_KEY not set in .env")

        client = genai.Client(api_key=api_key)

        # Build a single prompt string from messages
        parts = []
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                parts.append(f"[System]: {content}")
            elif role == "user":
                parts.append(f"[User]: {content}")
            elif role == "assistant":
                parts.append(f"[Assistant]: {content}")

        prompt = "\n".join(parts)

        response = client.models.generate_content(
            model=resolved_model,
            contents=prompt,
        )
        return response.text.strip()

    except EnvironmentError as exc:
        logger.warning("LLM unavailable: %s", exc)
        return f"[LLM unavailable: {exc}]"
    except Exception as exc:
        logger.error("LLM error: %s", exc)
        return f"[LLM error: {exc}]"


def _load_config_model() -> str:
    import json, pathlib
    cfg_path = pathlib.Path("config.json")
    if cfg_path.exists():
        try:
            return json.loads(cfg_path.read_text()).get("model", "")
        except Exception:
            pass
    return ""
