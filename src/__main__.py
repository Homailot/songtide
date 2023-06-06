import sys
from enum import Enum
from multiprocessing import Event, Process, Queue
from typing import Type

import pygame
import pygame_gui

from src.config import Configs
from src.field import MonsterField
from src.generative.indispensability import (
    basic_indispensability,
    indispensability,
    pulse_weights,
    time_signature_factors,
)
from src.monsters import Monster
from src.monsters.euclideanmonster import RattleSnare, ThumpFoot
from src.monsters.fractalmonster import (
    Boris,
    DarkEcho,
    EtherealEcho,
    FusionCore,
    HummingVenus,
    SonicScale,
)
from src.monsters.monsterinfo import MonsterInfo
from src.soundengine import soundengine
from src.ui import UI


class GameState(Enum):
    RUNNING = 0
    PAUSED = 1
    STOPPED = 2


class Game:
    def __init__(self) -> None:
        self.state = GameState.STOPPED
        self.frames_per_second = 60
        self.milliseconds_per_frame = 1000 / self.frames_per_second

        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.lag = 0.0
        self.state = GameState.RUNNING

        self.monster_info: dict[Type[Monster], MonsterInfo] = {}

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = GameState.STOPPED

            self.monster_field.process_events(event)
            self.ui.process_events(event)

    def render(self, screen: pygame.Surface):
        screen.fill("#5BC4A4")
        self.monster_field.render(screen)
        self.ui.render(screen)

        pygame.display.flip()

    def update(self):
        self.ui.update(self.delta_time)
        self.monster_field.update(self.delta_time)

    def handle_run(self, screen: pygame.Surface):
        self.process_events()

        while self.lag >= self.milliseconds_per_frame:
            self.update()
            self.lag -= self.milliseconds_per_frame

        self.render(screen)

    def start(self):
        configs = Configs()

        pygame.init()
        screen = pygame.display.set_mode((configs.screen_width, configs.screen_height))
        pygame.display.set_caption("Songtide")

        ethereal_echo_image = pygame.image.load(
            "resources/sprites/EtherealEcho.png"
        ).convert_alpha()

        dark_echo_image = pygame.image.load(
            "resources/sprites/DarkEcho.png"
        ).convert_alpha()

        boris_image = pygame.image.load("resources/sprites/Boris.png").convert_alpha()

        fusion_image = pygame.image.load(
            "resources/sprites/FusionCore.png"
        ).convert_alpha()

        humming_venus_image = pygame.image.load(
            "resources/sprites/HummingVenus.png"
        ).convert_alpha()

        thump_foot_image = pygame.image.load(
            "resources/sprites/ThumpFoot.png"
        ).convert_alpha()

        rattle_snare_image = pygame.image.load(
            "resources/sprites/RattleSnare.png"
        ).convert_alpha()

        sonic_scale_image = pygame.image.load(
            "resources/sprites/SonicScale.png"
        ).convert_alpha()

        self.monster_info[EtherealEcho] = MonsterInfo(
            "Ethereal Echo",
            "Mesmerizing creature that embodies the essence of music.<br>"
            "Its translucent body shimmers with delicate hues, "
            "reflecting the colors of the harmonies it creates",
            "#ethereal_button",
            ethereal_echo_image,
        )
        self.monster_info[DarkEcho] = MonsterInfo(
            "Dark Echo",
            "The Dark Echo is a haunting and mysterious creature that dwells within the shadows, "
            "emanating bone-chilling and ethereal sounds that send shivers down the spine.<br>"
            "Veiled in an aura of darkness, this enigmatic monster appears as a spectral entity, "
            "its form shifting and swirling like a nebulous mist.",
            "#dark_button",
            dark_echo_image,
        )
        self.monster_info[Boris] = MonsterInfo(
            "Boris",
            "Boris.",
            "#boris_button",
            boris_image,
        )
        self.monster_info[FusionCore] = MonsterInfo(
            "Fusion Core",
            "This extraordinary monster manifests itself as a living embodiment of a fusion reactor, "
            "radiating with intense and vibrant hues of energy.<br>"
            "Its body pulsates with a captivating glow, revealing intricate patterns reminiscent of "
            "swirling plasma and crackling arcs of electricity.",
            "#fusion_button",
            fusion_image,
        )
        self.monster_info[HummingVenus] = MonsterInfo(
            "Bowtied Starlet",
            "Its metallic surface gleams with a gentle shimmer, "
            "reflecting the light like a twinkling star.<br>"
            "This adorable extraterrestrial being hovers playfully through the air, "
            "emitting a soft hum that resonates with innocence and charm.",
            "#humming_button",
            humming_venus_image,
        )
        self.monster_info[SonicScale] = MonsterInfo(
            "Sonic Scale",
            "The Sonic Scale is a captivating and enigmatic creature that defies expectations.<br>"
            "At first glance, it resembles a beautifully crafted guitar, with sleek curves and strings that shimmer "
            "like polished silver. However, upon closer inspection, it becomes clear that this instrument-like creature is, "
            "in fact, a bass of extraordinary proportions.",
            "#sonic_button",
            sonic_scale_image,
        )
        self.monster_info[ThumpFoot] = MonsterInfo(
            "Thump Foot",
            "A mighty and thunderous creature, known for its powerful and earth-shaking stomps.<br>"
            "Its presence is announced by deep, "
            "reverberating thumps that echo through the surrounding terrain.",
            "#thump_button",
            thump_foot_image,
        )
        self.monster_info[RattleSnare] = MonsterInfo(
            "Rattle Snare",
            "The defining feature of the Rattle Snare is its tail, "
            "which is adorned with a series of small rattling appendages "
            "that create percussive beats.<br>Each movement of the tail sends "
            "forth a cascade of intricate and precise rattling sounds, forming a complex rhythmic tapestry.",
            "#rattle_button",
            rattle_snare_image,
        )

        self.manager = pygame_gui.UIManager(
            (configs.screen_width, configs.screen_height)
        )

        # print(pulse_weights(3, 4))

        stop_event = Event()
        monster_command_queue = Queue()
        clock_command_queue = Queue()
        monster_sound_queue = Queue()

        soundengine_process = Process(
            target=soundengine.start,
            args=(
                stop_event,
                monster_command_queue,
                clock_command_queue,
                monster_sound_queue,
            ),
        )
        soundengine_process.start()

        self.monster_field = MonsterField(monster_command_queue, monster_sound_queue)
        self.ui = UI(
            self.monster_field,
            clock_command_queue,
            monster_command_queue,
            self.monster_info,
        )

        running = True
        while running:
            match self.state:
                case GameState.RUNNING:
                    self.handle_run(screen)
                case GameState.STOPPED:
                    running = False
                case _:
                    pass

            self.delta_time = self.clock.tick(60)
            self.lag += self.delta_time

        stop_event.set()
        # soundengine_process.join()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.start()
