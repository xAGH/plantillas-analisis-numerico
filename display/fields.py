from typing import Dict, List, Tuple, Union

"""
Formato:
{
    "Operación": [
        (Nombre del campo): Valor por defecto
    ]
}
"""

OperationConfig = Dict[str, List[Tuple[str, Union[int, float, None]]]]

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
