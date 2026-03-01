import math

VALID_SYMBOLS = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
VALID_SYMBOLS["pi"] = math.pi
VALID_SYMBOLS["e"] = math.e
