import tkinter as tk
from typing import Type

from display.fields import OPERATIONS_CONFIG
from display.layout import (
    build_button,
    build_frame,
    build_label,
    build_operation_selector,
)
from display.styles import BG_COLOR, CREDITS_COLOR, ERROR_COLOR, SUCCESS_COLOR
from utils.calculate import (
    calculate_definite_integral,
    calculate_derivative,
    calculate_limit,
)


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

        try:
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

        except Exception as e:
            msg = f"Revisar: {str(e)}"
            self.error_message.config(text=msg)
