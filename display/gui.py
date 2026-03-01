import tkinter as tk
from tkinter import ttk
from typing import Type

from models import derivative


class CalculadoraAN:

    def __init__(self, root: Type[tk.Tk]):
        self.root = root
        self.build_root()
        self.build_select()
        self.build_fields_frame()
        self.build_math_buttons()
        self.build_exception_message()
        self.build_success_message()
        self.build_calculate_btn()
        self.update_fields()
        self.build_credits()

    def build_root(self):
        self.root.title("Calculadora de Análisis Numérico")
        self.root.geometry("520x500")
        self.root.configure(bg="#1e1e2f")
        tk.Label(
            self.root,
            text="Análisis Numérico",
            bg="#1e1e2f",
            fg="white",
            font=("Arial", 16, "bold"),
        ).pack(pady=15)

    def build_credits(self):
        tk.Label(
            self.root,
            text="Creado por Alejandro Giraldo Herrera",
            bg="#1e1e2f",
            fg="#404051",
            font=("Arial", 12, "bold"),
        ).pack(side="bottom")

    def build_fields_frame(self):
        self.fields_frame = tk.Frame(self.root, bg="#1e1e2f")
        self.fields_frame.pack()

    def build_select(self):
        select_template = tk.Label(
            self.root, text="Seleccione plantilla:", bg="#1e1e2f", fg="white"
        )
        select_template.pack()

        self.operation_type = tk.StringVar()
        options = ttk.Combobox(
            self.root,
            textvariable=self.operation_type,
            values=["Límite", "Derivada", "Integral definida"],
        )
        options.pack()
        options.bind("<<ComboboxSelected>>", self.update_fields)
        options.set("Límite")

    def build_exception_message(self):
        self.error_message = tk.Label(
            self.root, text="", fg="red", bg="#1e1e2f", font=("Arial", 10, "bold")
        )
        self.error_message.pack()

    def build_success_message(self):
        self.result = tk.Label(
            self.root, text="", fg="lightgreen", bg="#1e1e2f", font=("Arial", 12)
        )
        self.result.pack(pady=10)

    def build_calculate_btn(self):
        row = tk.Frame(self.root, bg="#1e1e2f")
        row.pack()

        tk.Button(
            row,
            text="Calcular",
            command=self.calculate,
            bg="#3a3a5f",
            fg="white",
            width=15,
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            row,
            text="Limpiar",
            command=lambda: (
                self.function_entry.delete(0, tk.END)
                if hasattr(self, "function_entry")
                else None
            ),
            bg="#ff6f59",
            fg="white",
            width=15,
        ).pack(side="left")

    def build_math_buttons(self):
        self.buttons_frame = tk.Frame(self.root, bg="#1e1e2f")
        self.buttons_frame.pack(pady=24)

        buttons = [
            ("π", "pi"),
            ("e", "e^()"),
            ("√", "sqrt()"),
            ("sin", "sin()"),
            ("cos", "cos()"),
            ("tan", "tan()"),
            ("log", "log()"),
            ("ln", "log()"),
            ("^", "^"),
        ]

        for text, value in buttons:
            btn = tk.Button(
                self.buttons_frame,
                text=text,
                width=5,
                command=lambda v=value: self.insert_in_function(v),
                bg="#3a3a5f",
                fg="white",
            )
            btn.pack(side="left", padx=3)

    def insert_in_function(self, value):
        if hasattr(self, "function_entry"):
            self.function_entry.insert(tk.INSERT, value)

    def clear(self):
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

    def create_field(self, text: str, default_value=None):
        label = tk.Label(self.fields_frame, text=text, bg="#1e1e2f", fg="white")
        label.pack()

        entry = tk.Entry(self.fields_frame, width=30)
        entry.pack(pady=5)

        if default_value is not None:
            entry.insert(0, str(default_value))

        if text == "Función f(x):":
            self.function_entry = entry

    def update_fields(self, event=None):
        fn = None

        if hasattr(self, "function_entry"):
            fn = self.function_entry.get()

        self.clear()

        operation = self.operation_type.get()

        self.create_field("Función f(x):", fn)

        if operation == "Límite":
            self.create_field("Tendencia (x →):")
            self.create_field("Precisión:", 0.0001)

        elif operation == "Derivada":
            self.create_field("Valor de x:")
            self.create_field("h:", 0.0001)
            self.create_field("Orden (1 o 2):", 1)

        elif operation == "Integral definida":
            self.create_field("Límite inferior:")
            self.create_field("Límite superior:")
            self.create_field("Intervalos (n):", 36)

    def get_values(self):
        return [
            w.get()
            for w in self.fields_frame.winfo_children()
            if isinstance(w, tk.Entry)
        ]

    def validate_value_type(self, var: str, value: str, check_type):

        if value == "":
            raise ValueError(f"Por favor ingrese el valor de {var}")

        try:
            return check_type(value)
        except:
            raise ValueError(
                f"El valor de {var} debe de ser un {check_type} válido.\nObtenido: {value}"
            )

    def calculate(self):
        self.error_message.config(text="")
        self.result.config(text="")
        res = "ok"

        try:
            operation = self.operation_type.get()
            values = self.get_values()

            if operation == "Límite":
                func, t, p = values
                t = self.validate_value_type("t", t, float)
                p = self.validate_value_type("p", p, float)
                # res = limite(func, t, p)

            elif operation == "Derivada":
                func, x, h, order = values
                x = self.validate_value_type("x", x, float)
                h = self.validate_value_type("h", h, float)
                order = self.validate_value_type("order", order, int)
                res = derivative(func, x, order, h)

            elif operation == "Integral definida":
                func, a, b, n = values
                a = self.validate_value_type("a", a, float)
                b = self.validate_value_type("b", b, float)
                n = self.validate_value_type("n", n, int)
                # res = integral_definida(func, a, b, n)

            else:
                raise ValueError("Seleccione un tipo de operación")

            self.result.config(text=f"Resultado: {res}")

        except Exception as e:
            self.error_message.config(text=f"Revisar: {str(e)}")
            self.error_message.config(text=f"Revisar: {str(e)}")
