# Multi-Tool AI Agent

## Overview

A modular, tool-using AI agent that routes natural-language queries to the right tool — calculator, file reader, summarizer, weather API, or GitHub API — and formats the result using Gemini. Built like a mini agent framework with a tool registry, persistent memory, config-driven loading, and structured logging.

## Architecture

```
User Input
    ↓
main.py
    ↓
agent/agent.py          ← orchestrates everything
    ↓
agent/tool_router.py    ← selects tool from registry
    ↓
agent/registry.py       ← tool registry (config-driven)
    ↓
tools/
  ├── calculator.py
  ├── file_reader.py
  ├── summarizer.py
  ├── weather.py
  └── github_tool.py
    ↓
agent/memory.py         ← persists conversation to memory.json
utils/api_client.py     ← Gemini wrapper
utils/logger.py         ← structured logging → logs/agent.log
```

## Features

- Tool Registry — all tools registered in one place, dynamically loaded by the router
- Config-driven — enable/disable tools via `config.json` without touching code
- Persistent Memory — every query and response saved to `memory.json` with timestamps; injected into LLM context for continuity
- Structured Logging — every step logged with `[AGENT]`, `[ROUTER]` tags to console and `logs/agent.log`
- Calculator — safe AST-based arithmetic, no `eval()`
- File Reader — reads local text files from `examples/` or current directory
- Text Summarizer — Gemini-powered with extractive fallback
- Weather — OpenWeatherMap current conditions
- GitHub — public repo stats via GitHub REST API
- CLI interface — interactive mode and single-query `-q` flag

## Folder Structure

```
multi-tool-ai-agent/
├── main.py
├── agent/
│   ├── agent.py
│   ├── tool_router.py
│   ├── registry.py
│   └── memory.py
├── tools/
│   ├── calculator.py
│   ├── file_reader.py
│   ├── summarizer.py
│   ├── weather.py
│   └── github_tool.py
├── utils/
│   ├── api_client.py
│   └── logger.py
├── examples/
│   └── sample.txt
├── logs/
├── memory.json
├── config.json
├── requirements.txt
└── .env
```

## Setup

```bash
# 1. Clone and enter the repo
git clone https://github.com/your-username/multi-tool-ai-agent.git
cd multi-tool-ai-agent

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API keys
# Edit .env and fill in your keys
GEMINI_API_KEY=your_gemini_key
OPENWEATHER_API_KEY=your_openweather_key
GITHUB_TOKEN=your_github_token   # optional
```

## Config

`config.json` controls which tools are active and agent behaviour:

```json
{
  "model": "gemini-2.0-flash",
  "tools_enabled": ["calculator", "file_reader", "summarizer", "weather", "github"],
  "logging": true,
  "memory": true
}
```

Remove a tool from `tools_enabled` to disable it without touching any code.

## How to Run

Interactive mode:
```bash
venv/bin/python main.py
```

Single query mode:
```bash
venv/bin/python main.py -q "calculate 25 * 48"
```

## Example Queries

```
You: calculate 25 * 48
Agent: 25 * 48 = 1200

You: read file sample.txt
Agent: --- examples/sample.txt ---
       Artificial intelligence (AI) is intelligence...

You: summarize Artificial intelligence is the simulation of human intelligence by machines...
Agent: AI refers to machines simulating human cognitive abilities...

You: github tensorflow/tensorflow
Agent: GitHub: tensorflow/tensorflow
         Stars: 194,427 ...

You: weather in Delhi
Agent: Weather in Delhi, IN:
         Haze, 34°C (feels like 38°C), humidity 52%
```

## Logging

Every query produces structured logs like:

```
[AGENT] User query received: calculate 25 * 48
[ROUTER] Query matched tool: calculator (keyword: 'calculate')
[AGENT] Selected tool: calculator
[AGENT] Tool 'calculator' executed successfully
[AGENT] Response returned for tool: calculator
```

Logs are saved to `logs/agent.log` and printed to console.

## Memory

All queries and responses are persisted to `memory.json` with timestamps:

```json
{
  "role": "user",
  "content": "github microsoft/vscode",
  "timestamp": "2026-04-01T22:15:38"
}
```

The agent injects the last 6 exchanges into the LLM context so it can reference previous conversations.

## Tools

| Tool | Trigger keywords | API key needed |
|------|-----------------|----------------|
| Calculator | calculate, compute, math | No |
| File Reader | read file, open file | No |
| Summarizer | summarize, summary, tldr | Yes (Gemini) |
| Weather | weather in/for/at | Yes (OpenWeatherMap) |
| GitHub | github, repo, repository | Optional |

## Future Improvements

- LLM-based tool routing (Gemini function calling)
- Tool permissions system (allow/deny per tool)
- Web interface (FastAPI + frontend)
- Plugin system for adding custom tools at runtime
- Authentication layer
