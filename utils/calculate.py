from display.validators import validate
from models.definite_integral import definite_integral
from models.derivative import derivative
from models.limit import limit


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
