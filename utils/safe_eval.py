import ast

from constants import VALID_SYMBOLS


def safe_eval(fn: str, x: float) -> float:

    if fn.strip() == "":
        raise ValueError("Por favor ingrese la función")

    fn = fn.replace("^", "**")
    node = ast.parse(fn, mode="eval")

    allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Call,
        ast.Name,
        ast.Load,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Pow,
        ast.USub,
        ast.UAdd,
        ast.Constant,
    )

    for subnode in ast.walk(node):

        if not isinstance(subnode, allowed_nodes):
            raise ValueError(f"La expresión '{subnode}' no es permitida")

        if isinstance(subnode, ast.Name):
            if subnode.id not in VALID_SYMBOLS and subnode.id != "x":
                raise ValueError(f"'{subnode.id}' no está permitido.")

        if isinstance(subnode, ast.Call):
            if not isinstance(subnode.func, ast.Name):
                raise ValueError("Llamada inválida.")
            if subnode.func.id not in VALID_SYMBOLS:
                raise ValueError(f"Función '{subnode.func.id}' no permitida.")

    return eval(
        compile(node, "<string>", "eval"),
        {"__builtins__": {}},
        {**VALID_SYMBOLS, "x": x},
    )
