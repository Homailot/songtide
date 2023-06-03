from abc import ABC, abstractmethod

from src.soundengine.sound import Sound


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

    @abstractmethod
    def __init__(self, position: tuple[float, float], channel: int = 0):
        self.muted = False
        self.position = position
        self.channel = channel

    @abstractmethod
    def generate_next_sound(self, current_beat: float):
        """Generates the next sound for the monster.
        This is so that monsters can pre-generate their sounds
        and then play them when needed.

        Parameters
        ----------
        current_beat : float
            The current beat of the clock.
        """
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
