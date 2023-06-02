from time import sleep, perf_counter
import fluidsynth
from multiprocessing import Event
from src import clock
import os
from src.config import Configs

def start(stop_event: Event, bpm: int):
    configs = Configs()

    fs = fluidsynth.Synth(samplerate=44100.0, channels=128)

    fs.setting("synth.sample-rate", 44100.0)
    fs.setting("sytnh.reverb.active", 1)
    fs.setting("synth.chorus.active", 1)

    fs.start(driver="pipewire", midi_driver="jack", device=0)
    
    fs.setting("synth.gain", 0.67)

    fs.set_reverb(0.26, 0.62, 0.86, 1)
    fs.set_chorus(22, 0.23, 1, 6.8, 0)

    sfid = fs.sfload(configs.soundfont_path)
    fs.program_select(0, sfid, 0, 0)

    clock = clock.Clock(bpm)
    while True:
        current_beat = clock.tick()
        if stop_event.is_set():
            break
    
    print("Goodbye world!")

    for i in range(128):
        fs.all_notes_off(i)

    fs.delete()
