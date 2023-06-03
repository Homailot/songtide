from abc import ABC, abstractmethod
from typing import Callable

from src.plugins import MonsterPlugin
from src.soundengine.sound import Sound


class PluginParameter:
    """A parameter for a plugin.
    This is used to store the parameters of a plugin.
    """

    def __init__(
        self,
        name: str,
        value: Callable[[], float],
        min: float,
        max: float,
        save: Callable[[float], None],
        step: float = 0.1,
    ):
        self.name = name
        self.value = value
        self.min = min
        self.max = max
        self.save = save
        self.step = step


class Monster(ABC):
    """
    A monster is a sound generator that can be placed on the screen.

    Attributes
    ----------
    muted : bool
        Whether the monster is muted or not.
    position : tuple[float, float]
        The position of the monster on the screen.
        It is a tuple of the x and y coordinates,
        ranging from 0 to 1.
    """

    next_sound: Sound | None = None
    plugins: list[MonsterPlugin] = []
    plugin_parameters: list[PluginParameter] = []

    @abstractmethod
    def __init__(self, position: tuple[float, float], channel: int = 0):
        self.muted = False
        self.position = position
        self.channel = channel

    def add_plugin(self, plugin: MonsterPlugin):
        """Adds a plugin to the monster.

        Parameters
        ----------
        plugin : MonsterPlugin
            The plugin to add.
        """
        self.plugins.append(plugin)

    def generate_next_sound(self, current_beat: float):
        """Generates the next sound for the monster.
        This is so that monsters can pre-generate their sounds
        and then play them when needed.

        Parameters
        ----------
        current_beat : float
            The current beat of the clock.
        """
        if self.next_sound is None:
            note = 0.0
            duration = 0.0
            rest = 0.0

            for plugin in self.plugins:
                note, duration, rest = plugin.transform(note, duration, rest)

            self.next_sound = self.generate_next_sound_internal(
                current_beat, note, duration, rest
            )

    @abstractmethod
    def generate_next_sound_internal(
        self, current_beat: float, note: int, duration: float, rest: float
    ) -> Sound:
        pass

    def make_sound(self, current_beat: float) -> Sound | None:
        """Makes a sound for the monster.
        If the monster is muted, then it will not make a sound.
        If it is not time for the monster to make a sound,
        then it will not make a sound.

        This just gets the next sound from the monster, generated from
        generate_next_sound, and returns it, if it is time for the monster
        to make a sound.

        Parameters
        ----------
        current_beat : float
            The current beat of the clock.

        Returns
        -------
        Sound | None
            The sound that the monster made.
            If the monster did not make a sound, then None is returned.
        """

        if not self.muted and current_beat >= self.next_sound.init:
            if self.next_sound == None:
                self.generate_next_sound(current_beat)

            print(f"Monster {self} made sound {self.next_sound}")
            sound = self.next_sound
            self.next_sound = None
            return sound
        elif self.muted and current_beat >= self.next_sound.init:
            self.next_sound = None

        return None

    def mute(self):
        self.muted = True

    def unmute(self):
        self.muted = False
