import math


def eval_function(fn: str, value: float):
    fn = fn.replace(" ", "")
    safe_dict = {
        "x": value,
        "pi": math.pi,
        "E": math.e,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "sqrt": math.sqrt,
    }

    return eval(fn, {"__builtins__": None}, safe_dict)


def main():
    fn = "(sqrt(x + 1) - 2) / x - 3"  # Función
    a = 3  # Tendencia
    E = 1e-6  # Precisión
    lower = a - E
    upper = a + E
    l1 = eval_function(fn, lower)
    l2 = eval_function(fn, upper)
    exists = (l1 * l2) >= 0
    average = str((l1 + l2) / 2)
    result = average if exists else "El límite no existe"

    print(f"f(x) = {fn}")
    print(f"Tendencia: {a}")
    print(f"Precisión: {E}")
    print(f"a - E = {lower}")
    print(f"a + E = {upper}")
    print(f"f(a - E) = {l1}")
    print(f"f(a + E) = {l2}")
    print(f"Resultado: {result}")


if __name__ == "__main__":
    main()
