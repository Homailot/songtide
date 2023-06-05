from src.generative.euclidean import euclidean_rhythm
from src.plugins import MonsterPlugin


class EuclideanRhythmPlugin(MonsterPlugin):
    """A Plugin for a monster
    These plugins alter the notes, durations, and rests of a sound that a monster makes.

    Attributes
    ----------
    steps : int
        The number of steps in the rhythm.
    hits : int
        The number of hits in the rhythm.
    accents : int
        The number of accents in the rhythm.
    rotation : int
        The rotation of the rhythm.
    accent_rotation : int
        The accent rotation of the rhythm.
    """

    def __init__(
        self, steps: int, hits: int, accents: int, rotation: int, accent_rotation: int
    ):
        self.steps = steps
        self.hits = hits
        self.accents = accents
        self.rotation = rotation
        self.accent_rotation = accent_rotation
        self.rhythm = euclidean_rhythm(steps, hits, accents, rotation, accent_rotation)
        self.counter = 0

    def reset_rhythm(self):
        self.rhythm = euclidean_rhythm(
            self.steps, self.hits, self.accents, self.rotation, self.accent_rotation
        )
        self.counter = self.counter % self.steps

    def set_steps(self, steps: int):
        self.steps = steps
        self.reset_rhythm()

    def set_hits(self, hits: int):
        self.hits = hits
        self.reset_rhythm()

    def set_accents(self, accents: int):
        self.accents = accents
        self.reset_rhythm()

    def set_rotation(self, rotation: int):
        self.rotation = rotation
        self.reset_rhythm()

    def set_accent_rotation(self, accent_rotation: int):
        self.accent_rotation = accent_rotation
        self.reset_rhythm()

    def get_steps(self) -> int:
        return self.steps

    def get_hits(self) -> int:
        return self.hits

    def get_accents(self) -> int:
        return self.accents

    def get_rotation(self) -> int:
        return self.rotation

    def get_accent_rotation(self) -> int:
        return self.accent_rotation

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
        # Find the next non-zero value in the rhythm
        while self.rhythm[self.counter] == 0:
            self.counter += 1
            self.counter %= self.steps

        note = self.rhythm[self.counter]

        # Find how long the note should be
        self.counter += 1
        self.counter %= self.steps
        rest = 0
        while self.rhythm[self.counter] == 0:
            rest += duration
            self.counter += 1
            self.counter %= self.steps

        result = (
            note,
            duration,
            rest,
        )
        return result
