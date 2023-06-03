import os
from threading import Lock

from dotenv import load_dotenv


class SingletonMeta(type):
    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Configs(metaclass=SingletonMeta):
    soundfont_path: str = None
    screen_width: int = None
    screen_height: int = None
    midi_driver: str = None
    audio_driver: str = None

    def __init__(self) -> None:
        load_dotenv()

        self.soundfont_path = os.getenv("SOUNDFONT_PATH", "soundfonts/EarthBound.sf2")
        self.screen_width = int(os.getenv("SCREEN_WIDTH", 1280))
        self.screen_height = int(os.getenv("SCREEN_HEIGHT", 700))
        self.midi_driver = os.getenv("MIDI_DRIVER", "jack")
        self.audio_driver = os.getenv("AUDIO_DRIVER", "pipewire")
