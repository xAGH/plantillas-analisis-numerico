from utils.safe_eval import safe_eval


def derivative(raw_fn: str, x: float, order=1, h=1e-5):
    fn = lambda var: safe_eval(raw_fn, var)

    if order == 1:
        return (fn(x + h) - fn(x - h)) / (2 * h)

    elif order == 2:
        return (fn(x + h) - 2 * fn(x) + fn(x - h)) / (h**2)

    else:
        raise ValueError("Solo se permite orden 1 o 2")
