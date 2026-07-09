"""
GrokCalci — a simple command-line calculator.
Supports +, -, *, /, **, %, and parentheses.
"""

import ast
import operator
import re
import sys


# Allowed binary operations
_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operations
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


class SafeEvaluator(ast.NodeVisitor):
    """Evaluate arithmetic expressions without using eval()."""

    def visit_Expression(self, node: ast.Expression):
        return self.visit(node.body)

    def visit_Constant(self, node: ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant: {node.value!r}")

    def visit_BinOp(self, node: ast.BinOp):
        op_type = type(node.op)
        if op_type not in _OPS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        left = self.visit(node.left)
        right = self.visit(node.right)
        try:
            return _OPS[op_type](left, right)
        except ZeroDivisionError as exc:
            raise ValueError("Division by zero") from exc

    def visit_UnaryOp(self, node: ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _UNARY_OPS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _UNARY_OPS[op_type](self.visit(node.operand))

    def generic_visit(self, node):
        raise ValueError(f"Unsupported expression: {type(node).__name__}")


def calculate(expression: str) -> float:
    """
    Evaluate a math expression string safely.

    Args:
        expression: Arithmetic expression (e.g. "2 + 3 * 4")

    Returns:
        The numeric result.

    Raises:
        ValueError: If the expression is empty, invalid, or unsafe.
    """
    expr = expression.strip()
    if not expr:
        raise ValueError("Empty expression")

    # Normalize common symbols
    expr = expr.replace("×", "*").replace("÷", "/").replace("^", "**")

    # Only digits, arithmetic operators, parentheses, and whitespace
    if re.search(r"[^0-9+\-*/%.() \t]", expr):
        raise ValueError("Expression contains invalid characters")

    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression: {expression}") from exc

    result = SafeEvaluator().visit(tree)
    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result


def format_result(value) -> str:
    """Format a result for display."""
    if isinstance(value, float):
        # Avoid long floating-point tails when reasonable
        text = f"{value:.12g}"
        return text
    return str(value)


def run_repl() -> None:
    """Interactive calculator loop."""
    print("GrokCalci — Simple Calculator")
    print("Enter expressions like: 2 + 3 * 4")
    print("Type 'help' for operators, 'quit' or 'exit' to leave.\n")

    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not line:
            continue
        if line.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if line.lower() in ("help", "?"):
            print("Operators: +  -  *  /  //  %  ** (or ^)  ( )")
            print("Examples:  10 / 3   |   (2+3)*4   |   2^8")
            continue

        try:
            result = calculate(line)
            print(format_result(result))
        except ValueError as exc:
            print(f"Error: {exc}")


def main(argv: list[str] | None = None) -> int:
    """Entry point: one-shot expression args, or interactive mode."""
    args = argv if argv is not None else sys.argv[1:]

    if args:
        expression = " ".join(args)
        try:
            result = calculate(expression)
            print(format_result(result))
            return 0
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1

    run_repl()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
