from math import sqrt


def number_to_base(num: int, base: int) -> list[int]:
    """Converts a number to a list of digits in a given base.

    Parameters
    ----------
    num : int
        The number to convert.

    base : int
        The number base.

    Returns
    -------
    list[int]
        A list of digits in the given base.
    """
    if num == 0:
        return [0]

    digits = []
    while num:
        digits.append(int(num % base))
        num //= base

    return digits[::-1]


def sum_digits_base(num: int, base: int) -> int:
    """Sums the digits of a number in a given base.

    Parameters
    ----------
    num : int
        The number to sum the digits of.

    base : int
        The number base.

    Returns
    -------
    int
        The sum of the digits of the number in the given base.
    """
    digits = number_to_base(num, base)
    return sum(digits)


def morse_thue_value(counter: int, base: int, multiplier: int) -> int:
    """Generates the Morse-Thue value for a given counter.

    Parameters
    ----------
    counter : int
        The counter value.

    base : int
        The number base

    multiplier : int
        The multiplier value.

    Returns
    -------
    int
        The Morse-Thue value.
    """
    counter = counter * multiplier
    return sum_digits_base(counter, base)


def logistic_map(x: float, k: float) -> float:
    """Calculates the logistic map for a given x and k.

    Parameters
    ----------
    x : float
        The x value.

    k : float
        The k value.

    Returns
    -------
    float
        The logistic map value.
    """
    return k * x * (1 - x)


def one_over_f(x: float, n: float, prev_logistic: float) -> tuple[float, float]:
    """Calculates the one over f value for a given x and n.

    Parameters
    ----------
    x : float
        The x value.
    n : float
        The n value.
    prev_logistic : float
        The previous logistic map value.

    Returns
    -------
    tuple[float, float]
        The one over f value, and the logistic map value.
    """
    r = logistic_map(prev_logistic, 4)
    return ((x * n) + (sqrt(1 - n**2) * r), r)
