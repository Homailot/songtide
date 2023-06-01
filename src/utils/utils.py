def octaver(scale: list[int], num_octaves: int, index: int) -> int:
    """Octaves a note.

    Parameters
    ----------
    scale : list[int]
        The scale to use for the octave.

    num_octaves : int
        The number of octaves to use.

    index : int
        The index to octave.

    Returns
    -------
    int
        The octaved note.
    """
    octave = index // len(scale)
    if octave >= num_octaves:
        octave = num_octaves - 1
        index = len(scale) - 1

    return scale[index] + 12 * octave