from abc import ABC, abstractmethod
from typing import Callable

from src.clock import Clock
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
    initialized: bool = False
    plugins: list[MonsterPlugin] = []
    plugin_parameters: list[PluginParameter] = []
    last_beat: float = 0.0
    last_duration: float = 0.0
    last_rest: float = 0.0
    last_bar: int = 0

    @abstractmethod
    def __init__(self, position: tuple[float, float], channel: int = 0):
        self.muted = False
        self.position = position
        self.channel = channel
        self.match_downbeat = True

    @abstractmethod
    def change_position(self, position: tuple[float, float]):
        """Changes the position of the monster.

        Parameters
        ----------
        position : tuple[float, float]
            The new position of the monster.
        """
        pass

    def initialize(self, current_beat: float):
        if not self.initialized:
            self.last_beat = int(current_beat + 1)

            self.initialized = True

    def add_plugin(self, plugin: MonsterPlugin):
        """Adds a plugin to the monster.

        Parameters
        ----------
        plugin : MonsterPlugin
            The plugin to add.
        """
        self.plugins.append(plugin)

    def generate_next_sound(self, clock: Clock):
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

            next_beat = self.last_beat + self.last_duration + self.last_rest

            self.next_sound = self.generate_next_sound_internal(
                next_beat, note, duration, rest
            )

            next_bar = int(
                clock.beat_to_bar(
                    self.next_sound.init + self.next_sound.duration + rest
                )
            )
            # if self.match_downbeat and next_bar > self.last_bar:
            #     beats_to_bar = clock.remaining_beats_to_bar(next_beat)
            #     self.next_sound.duration = beats_to_bar
            #     rest = 0

            self.last_beat = next_beat
            self.last_bar = next_bar
            self.last_duration = self.next_sound.duration
            self.last_rest = rest

    @abstractmethod
    def generate_next_sound_internal(
        self, next_beat: float, note: int, duration: float, rest: float
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
            if self.next_sound is None:
                self.generate_next_sound(current_beat)

            sound = self.next_sound
            self.next_sound = None
            return sound

        if self.muted and current_beat >= self.next_sound.init:
            self.next_sound = None

        return None

    def mute(self):
        self.muted = True

    def unmute(self):
        self.muted = False
