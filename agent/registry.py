"""
Tool Registry — single source of truth for all available tools.
Each tool entry defines its handler, keywords, and metadata.
Config-driven: tools can be enabled/disabled via config.json.
"""
import json
import logging
import pathlib

logger = logging.getLogger(__name__)

from tools.calculator import run as calculator_run
from tools.file_reader import run as file_reader_run
from tools.summarizer import run as summarizer_run
from tools.weather import run as weather_run
from tools.github_tool import run as github_run

# Master registry — order matters (higher priority first)
_ALL_TOOLS = {
    "github": {
        "handler": github_run,
        "description": "Get GitHub repository info",
        "keywords": ["github", "repo", "repository", "stars", "forks"],
    },
    "weather": {
        "handler": weather_run,
        "description": "Get current weather for a city",
        "keywords": ["weather", "temperature", "forecast", "climate"],
    },
    "summarizer": {
        "handler": summarizer_run,
        "description": "Summarize a block of text",
        "keywords": ["summarize", "summary", "tldr", "shorten"],
    },
    "file_reader": {
        "handler": file_reader_run,
        "description": "Read a local text file",
        "keywords": ["read file", "open file", "load file"],
    },
    "calculator": {
        "handler": calculator_run,
        "description": "Perform arithmetic calculations",
        "keywords": ["calculate", "compute", "math"],
    },
}


def _load_enabled_tools() -> list[str]:
    cfg = pathlib.Path("config.json")
    if cfg.exists():
        try:
            data = json.loads(cfg.read_text())
            return data.get("tools_enabled", list(_ALL_TOOLS.keys()))
        except Exception:
            pass
    return list(_ALL_TOOLS.keys())


def get_registry() -> dict:
    """Return only the tools that are enabled in config.json."""
    enabled = _load_enabled_tools()
    registry = {k: v for k, v in _ALL_TOOLS.items() if k in enabled}
    logger.debug("Active tools: %s", list(registry.keys()))
    return registry


def list_tools() -> list[dict]:
    """Return a summary of all registered tools for display."""
    return [
        {"name": k, "description": v["description"]}
        for k, v in get_registry().items()
    ]
