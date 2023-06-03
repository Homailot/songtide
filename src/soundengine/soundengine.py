from multiprocessing import Event

import fluidsynth

from src.clock import Clock
from src.config import Configs
from src.monsters import Monster
from src.monsters.fractalmonster import EtherealEcho
from src.soundengine.sound import Sound


def start(stop_event: Event, bpm: int):
    configs = Configs()

    fs = fluidsynth.Synth(samplerate=48000.0, channels=128)

    fs.setting("synth.sample-rate", 48000.0)
    fs.setting("synth.reverb.active", 1)
    fs.setting("synth.chorus.active", 1)

    fs.start(driver="pipewire", midi_driver="jack", device=0)

    fs.setting("synth.gain", 0.67)

    fs.set_reverb(0.26, 0.62, 0.86, 1)
    fs.set_chorus(22, 0.23, 1, 6.8, 0)

    sfid = fs.sfload(configs.soundfont_path)
    fs.program_select(0, sfid, 0, 32)

    monsters: list[Monster] = []
    sounds: list[Sound] = []

    monsters.append(EtherealEcho((0.5, 0.5)))

    clock = Clock(bpm)
    while True:
        current_beat = clock.tick()

        # TODO: MOVE THIS TO A SEPARATE THREAD
        for monster in monsters:
            monster.generate_next_sound(current_beat)

        sounds_to_remove: list[Sound] = []

        for sound in sounds:
            if sound.update(fs, current_beat):
                sounds_to_remove.append(sound)

        for sound in sounds_to_remove:
            sounds.remove(sound)

        for monster in monsters:
            sound = monster.make_sound(current_beat)
            if sound != None:
                sound.play(fs)
                sounds.append(sound)

        if stop_event.is_set():
            break

    print("Goodbye world!")

    for i in range(128):
        fs.all_notes_off(i)

    fs.delete()
