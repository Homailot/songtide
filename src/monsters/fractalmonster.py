from src.monsters.monster import Monster
from src.generative import fractal
from src.soundengine.sound import Sound

class FractalMonster(Monster):
    """Monster that generates a sound based on the Morse-Thue sequence.

    Attributes
    ----------
    base : int
        The number base.
    multiplier : int
        The multiplier value.
    duration_base : int
        The number base used for generating the duration.
    duration_multiplier : int
        The multiplier value used for generating the duration.
    counter : int
        The counter value. Indicates the current position in the sequence.
    starting_value : int
        The starting value for the sequence. It is a MIDI note,
        and is calculated based on the horizontal position of the monster.
    velocity : int
        The velocity of the note. It is calculated based on the vertical
        position of the monster.
    """

    def __init__(self, position: tuple[float, float], starting_duration: float = 1.0, channel: int = 0):
        super().__init__(position, channel)
        self.base = 2
        self.multiplier = 3
        self.duration_base = 2
        self.duration_multiplier = 1
        self.counter = 0
        self.starting_value = int(position[0] * 80) + 20
        self.velocity = int(position[1] * 80) + 20
        self.starting_duration = starting_duration

        self.last_beat = 0.0
        self.last_duration = 0.0

    def generate_next_sound(self, current_beat: float):
        """Generates the next sound for the monster.

        Parameters
        ----------
        current_beat : float
            The current beat of the clock.
        """
        if self.next_sound is None:
            note = fractal.morse_thue_value(self.counter, self.base, self.multiplier)
            duration = self.starting_duration / (fractal.morse_thue_value(self.counter, self.duration_base, self.duration_multiplier) + 1)
            print(f"Note: {note}, Duration: {duration}")

            next_beat = self.last_beat + self.last_duration
            self.last_beat = next_beat
            self.last_duration = duration

            self.next_sound = Sound(0, note + self.starting_value, self.velocity, next_beat + 0.05, duration)
            self.counter += 1
