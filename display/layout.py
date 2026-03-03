from tkinter import Button, Frame, Label, StringVar, Tk
from tkinter.ttk import Combobox
from typing import Callable, Dict, Optional, Union

from display.styles import BG_COLOR, BTN_COLOR, ERROR_COLOR, FG_COLOR


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
