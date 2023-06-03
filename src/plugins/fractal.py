from src.generative import fractal
from src.plugins import MonsterPlugin


class FractalNotePlugin(MonsterPlugin):
    """A Plugin for a monster
    These plugins alter the notes, durations, and rests of a sound that a monster makes.

    Attributes
    ----------
    base : int
        The base of the Morse-Thue sequence.
    multiplier : int
        The multiplier of the Morse-Thue sequence.
    counter : int
        The counter of the Morse-Thue sequence.
    """

    def __init__(self, base: int, multiplier: int):
        self.base = base
        self.multiplier = multiplier
        self.counter = 0

    def set_base(self, base: int):
        self.base = base

    def set_multiplier(self, multiplier: int):
        self.multiplier = multiplier

    def get_base(self) -> int:
        return self.base

    def get_multiplier(self) -> int:
        return self.multiplier

    def transform(
        self, _: int, duration: float, rest: float
    ) -> tuple[int, float, float]:
        """Transforms the note, duration, and rest of a sound that a monster makes.

        Parameters
        ----------
        note : int
            The note of the sound.
        duration : float
            The duration of the sound.
        rest : float
            The rest of the sound.

        Returns
        -------
        tuple[int, float, float]
            The transformed note, duration, and rest.
        """
        result = (
            fractal.morse_thue_value(self.counter, self.base, self.multiplier),
            duration,
            rest,
        )
        self.counter += 1
        return result


class FractalDurationPlugin(MonsterPlugin):
    """A Plugin for a monster
    These plugins alter the notes, durations, and rests of a sound that a monster makes.

    Attributes
    ----------
    base : int
        The base of the Morse-Thue sequence.
    multiplier : int
        The multiplier of the Morse-Thue sequence.
    counter : int
        The counter of the Morse-Thue sequence.
    """

    def __init__(
        self,
        base: int,
        multiplier: int,
        starting_duration: float = 1.0,
        max_duration: float = 3.0,
    ):
        self.base = base
        self.multiplier = multiplier
        self.starting_duration = starting_duration
        self.max_duration = max_duration
        self.counter = 0

    def set_base(self, base: int):
        self.base = base

    def set_multiplier(self, multiplier: int):
        self.multiplier = multiplier

    def set_starting_duration(self, starting_duration: float):
        self.starting_duration = starting_duration

    def set_max_duration(self, max_duration: float):
        self.max_duration = max_duration

    def get_base(self) -> int:
        return self.base

    def get_multiplier(self) -> int:
        return self.multiplier

    def get_starting_duration(self) -> float:
        return self.starting_duration

    def get_max_duration(self) -> float:
        return self.max_duration

    def transform(self, note: int, _: float, rest: float) -> tuple[int, float, float]:
        """Transforms the note, duration, and rest of a sound that a monster makes.

        Parameters
        ----------
        note : int
            The note of the sound.
        duration : float
            The duration of the sound.
        rest : float
            The rest of the sound.

        Returns
        -------
        tuple[int, float, float]
            The transformed note, duration, and rest.
        """
        duration = fractal.morse_thue_value(self.counter, self.base, self.multiplier)
        duration = duration % (self.max_duration)
        duration = self.starting_duration / (2**duration)
        self.counter += 1
        return (note, duration, rest)
