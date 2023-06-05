from src.monsters import Monster, PluginParameter
from src.plugins import ConstantRestPlugin
from src.plugins.fractal import FractalDurationPlugin, FractalNotePlugin
from src.plugins.octaver import OctavePlugin
from src.soundengine.sound import Sound


class EtherealEcho(Monster):
    """Monster that generates long, ethereal notes.

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
        super().__init__(position, 0)
        self.starting_value = int(position[0] * 80) + 20
        self.velocity = int(position[1] * 80) + 20

        self.fractal_note_plugin = FractalNotePlugin(3, 33)
        self.fractal_duration_plugin = FractalDurationPlugin(3, 33)
        self.constant_rest_plugin = ConstantRestPlugin(1)
        self.octave_plugin = OctavePlugin(0, 2)

        self.plugins = [
            self.fractal_note_plugin,
            self.fractal_duration_plugin,
            self.constant_rest_plugin,
            self.octave_plugin,
        ]

        self.plugin_parameters = [
            PluginParameter(
                "Jiveness",
                self.fractal_duration_plugin.get_starting_duration,
                0.5,
                3,
                self.fractal_duration_plugin.set_starting_duration,
                0.25,
            ),
            PluginParameter(
                "Quirkiness",
                self.fractal_duration_plugin.get_max_duration,
                2,
                5,
                self.fractal_duration_plugin.set_max_duration,
                1,
            ),
            PluginParameter(
                "Sleepiness",
                self.constant_rest_plugin.get_rest,
                0,
                2,
                self.constant_rest_plugin.set_rest,
                0.25,
            ),
            PluginParameter(
                "Vehemence",
                self.octave_plugin.get_intervals,
                0,
                6,
                self.octave_plugin.set_intervals,
                1,
            ),
            PluginParameter(
                "Wavelength",
                self.fractal_note_plugin.get_base,
                2,
                11,
                self.fractal_note_plugin.set_base,
                1,
            ),
            PluginParameter(
                "Skittishness",
                self.fractal_note_plugin.get_multiplier,
                2,
                33,
                self.fractal_note_plugin.set_multiplier,
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
        return Sound(0, note + self.starting_value, self.velocity, next_beat, duration)
