from multiprocessing import Event, Queue

import fluidsynth

from src.clock import Clock
from src.commands import ClockCommand, MonsterCommand
from src.config import Configs
from src.monsters import Monster
from src.soundengine.sound import MonsterSoundEvent, Sound


def start(
    stop_event: Event,
    monster_command_queue: "Queue[MonsterCommand]",
    clock_command_queue: "Queue[ClockCommand]",
    monster_sound_queue: "Queue[MonsterSoundEvent]",
    bpm: float,
):
    configs = Configs()

    fs = fluidsynth.Synth(samplerate=configs.sample_rate, channels=128)

    fs.setting("synth.sample-rate", configs.sample_rate)
    fs.setting("synth.reverb.active", 1)
    fs.setting("synth.chorus.active", 1)

    if configs.audio_driver == "jack":
        fs.setting("audio.jack.autoconnect", 1)

    print(f"Audio Driver: {configs.audio_driver}")
    print(f"MIDI Driver: {configs.midi_driver}")

    fs.start(driver=configs.audio_driver, midi_driver=configs.midi_driver, device=0)

    fs.setting("synth.gain", 0.67)

    fs.set_reverb(0.26, 0.62, 0.86, 1)
    fs.set_chorus(22, 0.23, 1, 6.8, 0)

    sfid = fs.sfload(configs.soundfont_path)
    fs.program_select(0, sfid, 0, 32)
    fs.program_select(1, sfid, 0, 45)
    fs.program_select(2, sfid, 128, 13)
    fs.program_select(3, sfid, 128, 6)

    monsters: dict[int, Monster] = {}
    sounds: list[tuple[int, Sound]] = []

    # monsters.append(EtherealEcho((0.5, 0.5)))

    clock = Clock(bpm)
    while True:
        current_beat = clock.tick()

        while not monster_command_queue.empty():
            command = monster_command_queue.get()
            command.execute(monsters)

            if command.id in monsters:
                monster = monsters[command.id]
                monster.initialize(current_beat)

        while not clock_command_queue.empty():
            command = clock_command_queue.get()
            old_bpm = clock.bpm
            print(f"Old BPM: {old_bpm}")
            command.execute(clock)
            print(f"New BPM: {clock.bpm}")

            for sound in sounds:
                sound[1].update_bpm(old_bpm, clock.bpm)

            for monster in monsters.values():
                monster.update_bpm(old_bpm, clock.bpm)

        current_beat = clock.tick()

        # TODO: MOVE THIS TO A SEPARATE THREAD, maybe?
        for monster in monsters.values():
            monster.generate_next_sound(current_beat)

            # Generate next sound can take some time, so we get the current beat again so it is accurate
            current_beat = clock.tick()

        sounds_to_remove: list[tuple[int, Sound]] = []

        for sound in sounds:
            if sound[1].update(fs, current_beat):
                sounds_to_remove.append(sound)
                monster_sound_queue.put(MonsterSoundEvent(sound[0], False))

        for sound in sounds_to_remove:
            sounds.remove(sound)

        for monster_id, monster in monsters.items():
            sound = monster.make_sound(current_beat)
            if sound is not None:
                sound.play(fs)
                sounds.append((monster_id, sound))
                monster_sound_queue.put(MonsterSoundEvent(monster_id, True))

        if stop_event.is_set():
            break

    print("Goodbye world!")

    for i in range(128):
        fs.all_notes_off(i)

    fs.delete()
