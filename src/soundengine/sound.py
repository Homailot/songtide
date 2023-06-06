import fluidsynth


class MonsterSoundEvent:
    def __init__(self, monster_id: int, on: bool):
        self.monster_id = monster_id
        self.on = on


class Sound:
    """A sound that can be played by the sound engine.

    Attributes
    ----------
    channel : int
        The MIDI channel to play the sound on.
    velocity : int
        The velocity of the sound.
    note : int
        The MIDI note to play.
    init : float
        The beat at which the sound was initialized.
    duration : float
        The duration of the sound in beats.
    """

    def __init__(
        self, channel: int, note: int, velocity: int, init: float, duration: float
    ):
        self.channel = channel
        self.velocity = velocity
        self.note = note
        self.init = init
        self.duration = duration

    def play(
        self, fs: fluidsynth.Synth, current_bar: float, pulse_weights: list[float]
    ):
        num_pulses = len(pulse_weights)
        velocity = int(
            self.velocity * pulse_weights[int(current_bar * num_pulses) % num_pulses]
        )
        fs.noteon(self.channel, self.note, velocity)

    def update(self, fs: fluidsynth.Synth, current_beat: float):
        if current_beat >= self.init + self.duration:
            fs.noteoff(self.channel, self.note)
            return True
        return False
