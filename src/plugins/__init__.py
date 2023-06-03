from abc import ABC, abstractmethod


class MonsterPlugin(ABC):
    """A Plugin for a monster
    These plugins alter the notes, durations, and rests of a sound that a monster makes.
    """

    @abstractmethod
    def transform(
        self, note: int, duration: float, rest: float
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
        pass


class ConstantRestPlugin(MonsterPlugin):
    """A Plugin for a monster
    These plugins alter the notes, durations, and rests of a sound that a monster makes.
    """

    def __init__(self, rest: float):
        self.rest = rest

    def set_rest(self, rest: float):
        self.rest = rest

    def get_rest(self) -> float:
        return self.rest

    def transform(
        self, note: int, duration: float, _: float
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
        return (note, duration, self.rest)
