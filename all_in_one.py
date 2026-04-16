import math
import tkinter as tk
from tkinter import Button, Frame, Label, StringVar, Tk
from tkinter.ttk import Combobox
from typing import Callable, Dict, List, Optional, Tuple, Type, Union

import sympy as sp
from mpmath import mp

mp.dps = 11  # dígitos decimales de precisión
VALID_SYMBOLS = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
VALID_SYMBOLS["pi"] = math.pi
VALID_SYMBOLS["e"] = math.e

BG_COLOR = "#1e1e2f"
FG_COLOR = "#e5e5e5"
BTN_COLOR = "#3a3a5f"
ERROR_COLOR = "#ff6f59"
SUCCESS_COLOR = "#8EF74C"
CREDITS_COLOR = "#404051"
OPERATIONS_CONFIG: Dict[str, List[Tuple[str, Union[int, float, None]]]] = {
    "Límite": [
        ("Tendencia (x →):", None),
        ("Precisión:", 0.0001),
    ],
    "Derivada": [
        ("Valor de x:", None),
        ("h:", 0.0001),
        ("Orden (1 o 2):", 1),
    ],
    "Integral definida": [
        ("Límite inferior:", None),
        ("Límite superior:", None),
        ("Intervalos (n):", 36),
    ],
    "Integral impropia (simpson)": [
        ("Límite inferior (float o -inf):", None),
        ("Límite superior (float o inf):", None),
        ("Intervalos (n):", 40),
    ],
    "Newton-Raphson": [
        ("Valor inicial x0:", None),
        ("Tolerancia:", 1e-6),
        ("Iteraciones máximas:", 100),
    ],
}


def safe_eval(fn: str, x_value):

    if fn.strip() == "":
        raise ValueError("Por favor ingrese la función")

    x = sp.symbols("x")

    try:
        sanitized = fn.lower().replace("^", "**").replace(" ", "")
        expr = sp.sympify(sanitized)
        result = expr.subs(x, x_value)
        result = sp.N(result)
    except Exception as e:
        raise ValueError(f"Error matemático: {e}")

    return result


# Modelos
def limit(raw_fn: str, trend: float, precision: float):
    lower = trend - precision
    upper = trend + precision
    l1 = safe_eval(raw_fn, lower)
    l2 = safe_eval(raw_fn, upper)
    exists = (l1 >= 0 and l2 >= 0) or (l1 <= 0 and l2 <= 0)
    average = str((l1 + l2) / 2)
    return average if exists else "El límite no existe"


def derivative(raw_fn: str, x: float, order=1, h=1e-5):
    fn = lambda var: safe_eval(raw_fn, var)

    if order == 1:
        return (fn(x + h) - fn(x - h)) / (2 * h)

    elif order == 2:
        return (fn(x + h) - 2 * fn(x) + fn(x - h)) / (h**2)

    else:
        raise ValueError("Solo se permite orden 1 o 2")


def definite_integral(
    raw_fn: str, lower_limit: float, upper_limit: float, intervals: int = 38
):
    precision = (upper_limit - lower_limit) / intervals
    frequencies = []
    previous_interval = lower_limit

    intervals_limit = intervals + 1

    for k in range(intervals_limit):
        xk = previous_interval if k == 0 else previous_interval + precision
        previous_interval = xk
        yk = safe_eval(raw_fn, xk)
        frequency = 1

        if k != 0 and k != intervals_limit:
            frequency = 2 if k % 2 == 0 else 4

        frequencies.append(yk * frequency)

    frequencies_sum = sum(frequencies)
    result = precision / 3 * frequencies_sum

    return result


def improper_integral_arctan(
    raw_fn: str,
    intervals: int = 40,
    epsilon: float = 0.0005,
):
    fn = lambda x: safe_eval(raw_fn, x)

    a = -math.pi / 2 + epsilon
    b = math.pi / 2 - epsilon

    h = (b - a) / intervals
    total = 0

    for i in range(intervals + 1):
        t = a + i * h

        x = math.tan(t)
        dx_dt = 1 / (math.cos(t) ** 2)  # sec^2(t)

        y = fn(x) * dx_dt

        weight = 1
        if i != 0 and i != intervals:
            weight = 4 if i % 2 != 0 else 2

        total += weight * y

    return (h / 3) * total


def newton_raphson(
    raw_fn: str,
    x0: float,
    tol: float = 1e-6,
    max_iter: int = 100,
):
    fn = lambda x: safe_eval(raw_fn, x)

    x = x0

    for _ in range(max_iter):
        fx = fn(x)
        dfx = derivative(raw_fn, x)

        if dfx == 0:
            raise ValueError("Derivada cero, no se puede continuar")

        x_new = x - fx / dfx

        if abs(x_new - x) < tol:
            return x_new

        x = x_new

    raise ValueError("No converge en el número máximo de iteraciones")


# Wrappers
def validate(name: str, value: str, cast: Callable = sp.Float):
    if not value:
        raise ValueError(f"Ingrese el valor de {name}")

    try:
        # Normalización básica
        sanitized = value.lower().replace("^", "**").replace(" ", "")

        # Permitir constantes como pi, e y operaciones
        expr = sp.sympify(sanitized)
        result = sp.N(expr)

        return cast(result)
    except Exception:
        raise ValueError(f"{name} debe ser un {cast.__name__} válido")


def calculate_limit(fn: str, trend: float, precision: float):
    x = validate("Tendencia", trend)
    h = validate("Precision", precision)

    return limit(fn, x, h)


def calculate_derivative(fn: str, x: float, precision: float, order: int):
    x = validate("x", x)
    h = validate("precision", precision)
    order = validate(
        "orden",
        order,
        int,
    )

    return derivative(fn, x, order, h)


def calculate_definite_integral(
    fn: str, lower_limit: float, upper_limit: float, intervals: int
):
    a = validate("limite inferior", lower_limit)
    b = validate("limite superior", upper_limit)
    n = validate("intérvalos", intervals, int)

    return definite_integral(fn, a, b, n)


def calculate_improper_simpson(
    fn: str, a: Optional[float], b: Optional[float], intervals: int
):
    a = None if a.lower() == "-inf" else validate("limite inferior", a)
    b = None if b.lower() == "inf" else validate("limite superior", b)
    n = validate("intervalos", intervals, int)
    return improper_integral_arctan(fn, n)


def calculate_newton(fn: str, x0, tol, max_iter):
    x0 = validate("x0", x0)
    tol = validate("tolerancia", tol)
    max_iter = validate("iteraciones", max_iter, int)

    return newton_raphson(fn, x0, tol, max_iter)


def build_frame(master: Union[Tk, Frame]):
    frame = Frame(master, bg=BG_COLOR)
    frame.pack()
    return frame


def build_button(
    master: Union[Tk, Frame],
    text: str,
    command: Callable[[], None],
    is_error=False,
    pack_options: Dict = {},
):
    button = Button(
        master,
        text=text,
        bg=ERROR_COLOR if is_error else BTN_COLOR,
        command=command,
        fg=FG_COLOR,
    )
    button.pack(**pack_options)
    return button


def build_label(
    master: Union[Tk, Frame],
    text: str,
    size: Optional[int] = None,
    fg=FG_COLOR,
    pack_options: Dict = {},
) -> Label:
    args = dict(
        master=master,
        text=text,
        bg=BG_COLOR,
        fg=fg,
    )

    if size != None:
        args["font"] = ("Arial", size, "bold")

    label = Label(**args)
    label.pack(**pack_options)
    return label


def build_operation_selector(
    master: Union[Tk, Frame], variable: StringVar, callback: Callable[[None], None]
):
    Label(
        master,
        text="Seleccione operación:",
        bg=BG_COLOR,
        fg=FG_COLOR,
    ).pack()

    combo = Combobox(
        master,
        textvariable=variable,
        values=[
            "Límite",
            "Derivada",
            "Integral definida",
            "Integral impropia (simpson)",
            "Newton-Raphson",
        ],
    )
    combo.pack()
    combo.bind("<<ComboboxSelected>>", callback)

    return combo


class CalculadoraAN:

    def __init__(self, root: Type[tk.Tk]):
        self.root = root
        self.fields = {}
        self.function_entry = None

        self._setup_root()

        build_label(root, "Análisis Numérico", size=16, pack_options=dict(pady=15))

        self.operation_type = tk.StringVar(value="Límite")
        build_operation_selector(
            root,
            self.operation_type,
            self.update_fields,
        )

        self.fields_frame = build_frame(root)

        self._build_messages()
        self._build_action_buttons()

        build_label(
            root,
            "Creado por Alejandro Giraldo Herrera",
            size=12,
            fg=CREDITS_COLOR,
            pack_options=dict(side="bottom"),
        )

        self.update_fields()

    def _setup_root(self):
        self.root.title("Calculadora de Análisis Numérico")
        self.root.geometry("520x500")
        self.root.configure(bg=BG_COLOR)

    def clear_fn(self):
        if hasattr(self, "function_entry"):
            self.function_entry.delete(0, tk.END)

    def update_fields(self, event=None):
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

        self.fields.clear()

        operation = self.operation_type.get()

        self._create_field("Función f(x):")

        for label, default in OPERATIONS_CONFIG.get(operation, []):
            self._create_field(label, default)

    def _create_field(self, label_text, default=None):
        tk.Label(
            self.fields_frame,
            text=label_text,
            bg=BG_COLOR,
            fg="white",
        ).pack()

        entry = tk.Entry(self.fields_frame)
        entry.pack(pady=5)

        if default is not None:
            entry.insert(0, str(default))

        self.fields[label_text] = entry

        if label_text == "Función f(x):":
            self.function_entry = entry

    def _build_messages(self):
        self.error_message = build_label(self.root, "", size=12, fg=ERROR_COLOR)
        self.result_message = build_label(
            self.root, "", size=14, fg=SUCCESS_COLOR, pack_options=dict(pady=10)
        )

    def _build_action_buttons(self):
        actions_btns_row = build_frame(self.root)
        build_button(
            actions_btns_row,
            "Calcular",
            self.calculate,
            pack_options=dict(side="left", padx=(0, 10)),
        )
        build_button(
            actions_btns_row,
            "Limpiar",
            self.clear_fn,
            is_error=True,
            pack_options=dict(side="left"),
        )

    def get_values(self):
        return [
            w.get()
            for w in self.fields_frame.winfo_children()
            if isinstance(w, tk.Entry)
        ]

    def calculate(self):
        try:
            self.error_message.config(text="")
            self.result_message.config(text="")

            operation = self.operation_type.get()
            values = self.get_values()
            operation_fn = None

            if operation == "Límite":
                operation_fn = calculate_limit
            elif operation == "Derivada":
                operation_fn = calculate_derivative
            elif operation == "Integral definida":
                operation_fn = calculate_definite_integral
            elif operation == "Integral impropia (simpson)":
                operation_fn = calculate_improper_simpson
            elif operation == "Newton-Raphson":
                operation_fn = calculate_newton

            result = operation_fn(*values)

            self.result_message.config(text=f"Resultado: {str(result)}")
        except Exception as e:
            self.error_message.config(text=f"Revisar: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    CalculadoraAN(root)
    root.mainloop()
