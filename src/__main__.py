import sys
from enum import Enum
from multiprocessing import Event, Process, Queue
from typing import Type

import pygame
import pygame_gui

from src.commands import CreateMonsterCommand
from src.config import Configs
from src.field import MonsterField
from src.monsters import Monster
from src.monsters.fractalmonster import EtherealEcho
from src.monsters.monsterinfo import MonsterInfo
from src.monsters.monsterrepository import MonsterRepository
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

        self.monster_info[EtherealEcho] = MonsterInfo(
            "Ethereal Echo",
            "Mesmerizing creature that embodies the essence of music.<br>"
            "Its translucent body shimmers with delicate hues, "
            "reflecting the colors of the harmonies it creates",
            "#ethereal_button",
            ethereal_echo_image,
        )

        self.manager = pygame_gui.UIManager(
            (configs.screen_width, configs.screen_height)
        )

        stop_event = Event()
        monster_command_queue = Queue()
        clock_command_queue = Queue()

        soundengine_process = Process(
            target=soundengine.start,
            args=(stop_event, monster_command_queue, clock_command_queue, 80),
        )
        soundengine_process.start()

        self.monster_field = MonsterField(monster_command_queue)
        self.ui = UI(self.monster_field, clock_command_queue, self.monster_info)

        # monster = EtherealEcho((0.4, 0.5))
        # id = self.monster_repository.add_monster(monster)
        # create_monster_command = CreateMonsterCommand(id, type(monster), (0.4, 0.5))
        # monster_command_queue.put(create_monster_command)

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
