import math

import numpy as np


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
