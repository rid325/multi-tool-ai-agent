"""
Summarizer tool — summarizes text using the LLM, or a simple extractive fallback.
"""
import re
from utils.api_client import chat_completion


def _extract_text(query: str) -> str:
    """Strip the 'summarize' command prefix and return the body text."""
    cleaned = re.sub(r"(?i)^(summarize|summary|tldr|shorten)\s*(this\s*)?(text\s*)?:?\s*", "", query).strip()
    return cleaned


def run(query: str) -> str:
    text = _extract_text(query)
    if not text:
        return "Please provide text to summarize, e.g. 'summarize <your text>'."

    # Try LLM summarization first
    try:
        messages = [
            {"role": "system", "content": "You are a concise summarizer. Summarize the user text in 2-3 sentences."},
            {"role": "user", "content": text},
        ]
        return chat_completion(messages)
    except Exception:
        pass

    # Extractive fallback: return first 3 sentences
    sentences = re.split(r"(?<=[.!?])\s+", text)
    summary = " ".join(sentences[:3])
    return f"[Extractive summary] {summary}"
