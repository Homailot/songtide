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
    octave = octave % num_octaves
    index = index % len(scale)

    return scale[index] + 12 * octave
