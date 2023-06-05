from time import perf_counter


class Clock:
    def __init__(self, bpm: float):
        self.bpm = bpm
        self.seconds_per_beat = 60 / self.bpm
        self.previous_time = perf_counter()
        self.current_beat = 0.0

    def update(self, delta_time: float):
        self.current_beat += delta_time / self.seconds_per_beat

    def change_bpm(self, bpm: float):
        self.bpm = bpm
        self.seconds_per_beat = 60 / self.bpm

    def tick(self) -> float:
        time = perf_counter()
        delta_time = time - self.previous_time
        self.previous_time = time

        self.update(delta_time)
        return self.current_beat
