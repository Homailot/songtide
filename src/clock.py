from time import perf_counter

from src.generative.indispensability import pulse_weights


class Clock:
    def __init__(self, bpm: float, nominator: int, denominator: int):
        self.change_bpm(bpm)
        self.change_signature(nominator, denominator)

        self.previous_time = perf_counter()

        self.current_beat = 0.0
        self.current_bar = 0.0

    def update(self, delta_time: float):
        delta_beat = delta_time / self.seconds_per_beat
        self.current_beat += delta_beat
        self.current_bar += delta_beat / self.beats_per_bar

    def change_bpm(self, bpm: float):
        self.bpm = bpm
        self.seconds_per_beat = 60 / self.bpm

    def change_signature(self, nominator: int, denominator: int):
        self.nominator = nominator
        self.denominator = denominator
        self.beats_per_bar = 4 / self.denominator * self.nominator

        self.pulse_weights = pulse_weights(nominator, denominator)

    def beat_to_bar(self, beat: float) -> float:
        return beat / self.beats_per_bar

    def remaining_beats_to_bar(self, beat: float) -> float:
        beat = beat % self.beats_per_bar
        return self.beats_per_bar - beat

    def tick(self) -> float:
        time = perf_counter()
        delta_time = time - self.previous_time
        self.previous_time = time

        self.update(delta_time)
        return self.current_beat
