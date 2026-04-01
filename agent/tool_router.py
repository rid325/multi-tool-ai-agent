"""
Tool Router — selects the right tool from the registry based on user query.
"""
import re
import logging
from agent.registry import get_registry

logger = logging.getLogger(__name__)


def route(query: str) -> str:
    """
    Match query against registered tool keywords.
    Returns tool name or 'chat' if no match found.
    """
    q = query.lower()
    registry = get_registry()

    for tool_name, meta in registry.items():
        for keyword in meta["keywords"]:
            if keyword in q:
                logger.info("[ROUTER] Query matched tool: %s (keyword: '%s')", tool_name, keyword)
                return tool_name

    # Arithmetic expression fallback — only if no tool matched
    if re.search(r"\d+\s*[\+\-\*\%\^]\s*\d+", q):
        logger.info("[ROUTER] Query matched tool: calculator (arithmetic regex)")
        return "calculator"

    logger.info("[ROUTER] No tool matched — routing to chat")
    return "chat"
