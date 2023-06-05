from src.monsters import Monster, PluginParameter
from src.plugins import ConstantDurationPlugin
from src.plugins.euclidean import EuclideanRhythmPlugin
from src.soundengine.sound import Sound


class ThumpFoot(Monster):
    """Monster that generates kick drum sounds.

    Attributes
    ----------
    starting_value : int
        The starting value for the sequence. It is a MIDI note,
        and is calculated based on the horizontal position of the monster.
    velocity : int
        The velocity of the note. It is calculated based on the vertical
        position of the monster.
    """

    def __init__(
        self,
        position: tuple[float, float],
    ):
        super().__init__(position, 2)
        self.starting_value = int(position[0] * 80) + 20
        self.velocity = int(position[1] * 80) + 20

        self.constant_duration_plugin = ConstantDurationPlugin(0.25)
        self.euclidean_rhythm_plugin = EuclideanRhythmPlugin(13, 5, 0, 0, 0)

        self.plugins = [
            self.constant_duration_plugin,
            self.euclidean_rhythm_plugin,
        ]

        self.plugin_parameters = [
            PluginParameter(
                "Jiveness",
                self.constant_duration_plugin.get_duration,
                0.0625,
                1,
                self.constant_duration_plugin.set_duration,
                0.0625,
            ),
            PluginParameter(
                "Recall",
                self.euclidean_rhythm_plugin.get_steps,
                1,
                16,
                self.euclidean_rhythm_plugin.set_steps,
                1,
            ),
            PluginParameter(
                "Footiness",
                self.euclidean_rhythm_plugin.get_hits,
                1,
                16,
                self.euclidean_rhythm_plugin.set_hits,
                1,
            ),
        ]

    def change_position(self, position: tuple[float, float]):
        """Changes the position of the monster.

        Parameters
        ----------
        position : tuple[float, float]
            The new position of the monster.
        """
        self.position = position
        self.starting_value = int(position[0] * 80) + 20
        self.velocity = int(position[1] * 80) + 20

    def generate_next_sound_internal(
        self, next_beat: float, note: int, duration: float, rest: float
    ) -> Sound:
        return Sound(
            self.channel, note + self.starting_value, self.velocity, next_beat, duration
        )
