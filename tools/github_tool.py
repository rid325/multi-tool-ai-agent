"""
GitHub tool — fetches public repo info via GitHub REST API.
Optionally uses GITHUB_TOKEN in .env to avoid rate limits.
"""
import re
import os
import requests


def _extract_repo(query: str) -> str:
    # Match owner/repo pattern
    match = re.search(r"([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)", query)
    return match.group(1) if match else ""


def run(query: str) -> str:
    repo = _extract_repo(query)
    if not repo:
        return "Please provide a repo in 'owner/repo' format, e.g. 'github tensorflow/tensorflow'."

    headers = {"Accept": "application/vnd.github+json"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"https://api.github.com/repos/{repo}"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        d = resp.json()
        return (
            f"GitHub: {d['full_name']}\n"
            f"  Description : {d.get('description') or 'N/A'}\n"
            f"  Stars       : {d['stargazers_count']:,}\n"
            f"  Forks       : {d['forks_count']:,}\n"
            f"  Open issues : {d['open_issues_count']:,}\n"
            f"  Language    : {d.get('language') or 'N/A'}\n"
            f"  URL         : {d['html_url']}"
        )
    except requests.HTTPError as e:
        return f"GitHub API error: {e.response.status_code} — {e.response.text}"
    except Exception as exc:
        return f"Failed to fetch repo info: {exc}"
