intervals = [
    [2, 2, 1, 2, 2, 2],  # major
    [2, 2, 2, 2, 2],  # whole tone
    [2, 2, 3, 2],  # pentatonic
    [3, 2, 1, 1, 3],  # blues
    [2, 1, 2, 2, 1, 2],  # minor
    [1, 2, 1, 2, 1, 2, 1],  # diminished
    [1, 2, 2, 2, 1, 2],  # phrygian
]


def compute_scale(key: int, intervals: list[int]) -> list[int]:
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

    for interval in intervals:
        scale.append(scale[-1] + interval)

    return scale
