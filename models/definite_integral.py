from utils.safe_eval import safe_eval


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
