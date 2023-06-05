"""This module contains functions for generating Euclidean rhythms.
"""


def euclidean_rhythm(
    steps: int, hits: int, accents: int, rotation: int = 0, accent_rotation: int = 0
) -> list[int]:
    """Generates an Euclidean rhythm with accents.

    Parameters
    ----------
    steps : int
        The total number of steps in the rhythm.

    hits : int
        The number of hits in the rhythm.

    accents : int
        The number of accents in the rhythm.

    rotation : int, optional
        The rotation value for the rhythm.
        It represents the number of steps to rotate the rhythm to the right.
        By default, it is set to 0, indicating no rotation.

    accent_rotation : int, optional
        The rotation value for the accents.
        It represents the number of steps to rotate the accents to the right.
        By default, it is set to 0, indicating no rotation.

    Returns
    -------
    list[int]
        A list representing the Euclidean rhythm, where 2 denotes an accent,
        1 denotes a hit and 0 denotes a rest.
        The length of the list is equal to the number of steps.
    """

    first_pass = euclidean_rhythm_simple(steps, hits, rotation)

    if accents > 0:
        accents = euclidean_rhythm_simple(hits, accents, accent_rotation)

        accent_index = 0
        for idx, note in enumerate(first_pass):
            if note == 1:
                first_pass[idx] += accents[accent_index]
                accent_index += 1

    return first_pass


def euclidean_rhythm_simple(steps: int, hits: int, rotation: int = 0) -> list[int]:
    """Generates an Euclidean rhythm.

    Parameters
    ----------
    steps : int
        The total number of steps in the rhythm.

    hits : int
        The number of hits in the rhythm.

    rotation : int, optional
        The rotation value for the rhythm.
        It represents the number of steps to rotate the rhythm to the right.
        By default, it is set to 0, indicating no rotation.

    Returns
    -------
    list[int]
        A list representing the Euclidean rhythm, where 1 denotes a hit and 0 denotes a rest.
        The length of the list is equal to the number of steps.
    """

    hits = min(steps, hits)

    pattern = []
    counts = []
    remainders = []
    divisor = steps - hits
    remainders.append(hits)
    level = 0

    while True:
        counts.append(divisor // remainders[level])
        remainders.append(divisor % remainders[level])
        divisor = remainders[level]
        level += 1
        if remainders[level] <= 1:
            break

    counts.append(divisor)

    def build(level):
        if level == -1:
            pattern.append(0)
        elif level == -2:
            pattern.append(1)
        else:
            for _ in range(0, counts[level]):
                build(level - 1)

            if remainders[level] != 0:
                build(level - 2)

    build(level)
    i = pattern.index(1)
    i = (i - rotation) % steps
    pattern = pattern[i:] + pattern[0:i]

    return pattern
