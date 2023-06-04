from enum import Enum


class Intervals(Enum):
    MAJOR: list[int] = [2, 2, 1, 2, 2, 2, 1]
    MINOR: list[int] = [2, 1, 2, 2, 1, 2, 2]


def compute_scale(key: int, intervals: Intervals) -> list[int]:
    """Computes a scale based on a given key and intervals.

    Parameters
    ----------
    key : int
        The key to use for the scale.

    intervals : Intervals
        The intervals to use for the scale.

    Returns
    -------
    list[int]
        The scale.
    """
    scale = [key]
    for interval in intervals.value:
        scale.append(scale[-1] + interval)

    return scale
