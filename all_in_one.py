import ast
import math
import tkinter as tk
from tkinter import Button, Frame, Label, StringVar, Tk
from tkinter.ttk import Combobox
from typing import Callable, Dict, List, Optional, Tuple, Type, Union

VALID_SYMBOLS = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
VALID_SYMBOLS["pi"] = math.pi
VALID_SYMBOLS["e"] = math.e


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


# Modelos
def limit(raw_fn: str, trend: float, precision: float):
    lower = trend - precision
    upper = trend + precision
    l1 = safe_eval(raw_fn, lower)
    l2 = safe_eval(raw_fn, upper)
    exists = (l1 * l2) >= 0
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

    for k in range(intervals + 1):
        xk = previous_interval if k == 0 else previous_interval + precision
        previous_interval = xk
        yk = safe_eval(raw_fn, xk)
        frequency = 1

        if k != 0 or k != intervals:
            frequency = 2 if k % 2 == 0 else 4

        frequencies.append(yk * frequency)

    frequencies_sum = sum(frequencies)
    result = precision / 3 * frequencies_sum

    return result


OperationConfig = Dict[str, List[Tuple[str, Union[int, float, None]]]]

BG_COLOR = "#1e1e2f"
FG_COLOR = "#e5e5e5"
BTN_COLOR = "#3a3a5f"
ERROR_COLOR = "#ff6f59"
SUCCESS_COLOR = "#8EF74C"
CREDITS_COLOR = "#404051"
OPERATIONS_CONFIG: OperationConfig = {
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
}


def validate(name: str, value: str, cast: Callable):
    if not value:
        raise ValueError(f"Ingrese el valor de {name}")

    try:
        return cast(value)
    except:
        raise ValueError(f"{name} debe ser un {cast.__name__} válido")


def calculate_limit(fn: str, trend: float, precision: float):
    x = validate("Tendencia", trend, float)
    h = validate("Precision", precision, float)

    return limit(fn, x, h)


def calculate_derivative(fn: str, x: float, precision: float, order: int):
    x = validate("x", x, float)
    h = validate("precision", precision, float)
    order = validate(
        "orden",
        order,
        int,
    )

    return derivative(fn, x, order, h)


def calculate_definite_integral(
    fn: str, lower_limit: float, upper_limit: float, intervals: int
):
    a = validate("limite inferior", lower_limit, float)
    b = validate("limite superior", upper_limit, float)
    n = validate("intérvalos", intervals, int)

    return definite_integral(fn, a, b, n)


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
        values=["Límite", "Derivada", "Integral definida"],
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

        result = operation_fn(*values)

        self.result_message.config(text=f"Resultado: {result}")


if __name__ == "__main__":
    root = tk.Tk()
    CalculadoraAN(root)
    root.mainloop()
