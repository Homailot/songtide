from time import sleep
import fluidsynth
from multiprocessing import Event
import os

def start(stop_event: Event):
    fs = fluidsynth.Synth(samplerate=44100.0)

    fs.setting("synth.sample-rate", 44100.0)

    fs.start(driver="pipewire", midi_driver="jack", device=0)

    
    fs.setting("synth.gain", 0.4)

    fs.set_reverb(0.26, 0.62, 0.86, 1)
    fs.set_chorus(22, 0.23, 1, 6.8, 0)

    sfid = fs.sfload("soundfonts/EarthBound.sf2")
    fs.program_select(0, sfid, 0, 0)
    print(os.getcwd())

    while True:
        fs.noteon(0, 60, 30)

        sleep(1)

        fs.noteoff(0, 60)

        sleep(1)

        if stop_event.is_set():
            break
    

    print("Goodbye world!")
    fs.delete()
