from src.plugins import MonsterPlugin
from src.utils import octaver
from src.utils.scales import Intervals, compute_scale


class OctavePlugin(MonsterPlugin):
    """A Plugin for a monster
    These plugins alter the notes, durations, and rests of a sound that a monster makes.
    """

    def __init__(self, intervals: int, num_octaves: int = 2):
        self.set_intervals(intervals)
        self.interval_num = intervals
        self.num_octaves = num_octaves

    def set_num_octaves(self, num_octaves: int):
        self.num_octaves = num_octaves

    def set_intervals(self, intervals: int):
        match intervals:
            case 0:
                self.scale = compute_scale(0, Intervals.Major)
            case 1:
                self.scale = compute_scale(0, Intervals.Minor)

        self.interval_num = intervals

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
        return (octaver(self.scale, self.num_octaves, note), duration, rest)
