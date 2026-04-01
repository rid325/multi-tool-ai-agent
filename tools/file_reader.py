"""
File Reader tool — reads a local text file and returns its contents.
"""
import re
import os


def _extract_filename(query: str) -> str:
    """Parse filename from queries like 'read file sample.txt'."""
    match = re.search(r"(?:read|open|load)\s+(?:file\s+)?(\S+)", query, re.IGNORECASE)
    if match:
        return match.group(1)
    # Last token fallback
    tokens = query.strip().split()
    return tokens[-1] if tokens else ""


def run(query: str) -> str:
    filename = _extract_filename(query)
    if not filename:
        return "Please specify a filename, e.g. 'read file sample.txt'."

    # Restrict to examples/ and current directory for safety
    search_paths = [filename, os.path.join("examples", filename)]
    for path in search_paths:
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                return f"--- {path} ---\n{content}"
            except Exception as exc:
                return f"Error reading '{path}': {exc}"

    return f"File '{filename}' not found. Looked in: {search_paths}"
