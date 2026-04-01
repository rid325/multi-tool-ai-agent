"""
Agent — orchestrates the tool registry, router, memory, and LLM.
"""
import json
import logging

from agent.tool_router import route
from agent.registry import get_registry
from agent import memory as mem
from utils.api_client import chat_completion
from utils.logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)


class Agent:
    def run(self, query: str) -> str:
        logger.info("[AGENT] User query received: %s", query)
        mem.append("user", query)

        tool_name = route(query)

        if tool_name == "chat":
            response = self._llm_chat(query)
        else:
            response = self._run_tool(tool_name, query)

        mem.append("assistant", response)
        logger.info("[AGENT] Response returned for tool: %s", tool_name)
        return response

    def _run_tool(self, tool_name: str, query: str) -> str:
        registry = get_registry()
        tool = registry.get(tool_name)
        if not tool:
            logger.error("[AGENT] Tool '%s' not found in registry", tool_name)
            return f"Tool '{tool_name}' is not available."

        logger.info("[AGENT] Selected tool: %s", tool_name)
        try:
            result = tool["handler"](query)
            logger.info("[AGENT] Tool '%s' executed successfully", tool_name)
            return json.dumps(result, indent=2) if isinstance(result, dict) else str(result)
        except Exception as exc:
            logger.error("[AGENT] Tool '%s' failed: %s", tool_name, exc)
            return f"Error running {tool_name}: {exc}"

    def _llm_chat(self, query: str) -> str:
        logger.info("[AGENT] Selected tool: chat (LLM)")
        # Inject memory context into system prompt
        memory_ctx = mem.get_summary()
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant with access to tools. "
                    + (f"\n\n{memory_ctx}" if memory_ctx else "")
                ),
            }
        ]
        messages += mem.get_recent(n=6)
        response = chat_completion(messages)
        logger.info("[AGENT] LLM responded successfully")
        return response
