from typing import Callable


def validate(name: str, value: str, cast: Callable):
    if not value:
        raise ValueError(f"Ingrese el valor de {name}")

    try:
        return cast(value)
    except:
        raise ValueError(f"{name} debe ser un {cast.__name__} válido")
