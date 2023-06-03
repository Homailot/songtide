import fluidsynth


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

    def play(self, fs: fluidsynth.Synth):
        fs.noteon(self.channel, self.note, self.velocity)

    def update(self, fs: fluidsynth.Synth, current_beat: float):
        if current_beat >= self.init + self.duration:
            fs.noteoff(self.channel, self.note)
            return True
        return False

    def update_bpm(self, old_bpm: float, new_bpm: float):
        self.init = self.init * old_bpm / new_bpm
        self.duration = self.duration * old_bpm / new_bpm
