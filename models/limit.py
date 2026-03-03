from utils.safe_eval import safe_eval


def limit(raw_fn: str, trend: float, precision: float):
    lower = trend - precision
    upper = trend + precision
    print(lower)
    print(upper)
    l1 = safe_eval(raw_fn, lower)
    l2 = safe_eval(raw_fn, upper)
    print(l1)
    print(l2)
    exists = (l1 * l2) >= 0
    average = str((l1 + l2) / 2)
    return average if exists else "El límite no existe"
