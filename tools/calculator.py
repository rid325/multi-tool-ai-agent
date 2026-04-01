"""
Calculator tool — safely evaluates arithmetic expressions from natural language.
"""
import re
import ast
import operator

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def _safe_eval(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp):
        return _OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp):
        return _OPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")


def _extract_expression(query: str) -> str:
    """Pull the math expression out of a natural-language query."""
    # Strip common prefixes
    cleaned = re.sub(r"(?i)^(calculate|compute|what is|eval|math)\s*", "", query).strip()
    # Keep only valid math characters
    expr = re.sub(r"[^0-9\.\+\-\*\/\%\^\(\)\s]", "", cleaned).strip()
    return expr


def run(query: str) -> str:
    expr = _extract_expression(query)
    if not expr:
        return "Could not find a math expression in your query."
    try:
        tree = ast.parse(expr, mode="eval")
        result = _safe_eval(tree.body)
        return f"{expr} = {result}"
    except Exception as exc:
        return f"Could not evaluate '{expr}': {exc}"
