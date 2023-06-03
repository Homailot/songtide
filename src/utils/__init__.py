from typing import Any


class Octaver(object):
    def __init__(self, scale: list[int], num_octaves: int) -> None:
        self.scale = scale
        self.num_octaves = num_octaves

    def __call__(self, index: int) -> int:
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
        octave = index // len(self.scale)
        if octave >= self.num_octaves:
            octave = self.num_octaves - 1
            index = len(self.scale) - 1
        index = index % len(self.scale)

        return self.scale[index] + 12 * octave
