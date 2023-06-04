import sys
from enum import Enum
from multiprocessing import Event, Process, Queue
from typing import Type

import pygame
import pygame_gui

from src.commands import CreateMonsterCommand
from src.config import Configs
from src.monsters import Monster
from src.monsters.fractalmonster import EtherealEcho
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

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = GameState.STOPPED

            self.ui.process_events(event)

    def render(self, screen: pygame.Surface):
        screen.fill("#5BC4A4")
        self.ui.render(screen)

        pygame.display.flip()

    def update(self):
        self.ui.update(self.delta_time)
        pass

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

        self.manager = pygame_gui.UIManager(
            (configs.screen_width, configs.screen_height)
        )
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.lag = 0.0
        self.monster_repository = MonsterRepository()
        self.state = GameState.RUNNING

        stop_event = Event()
        monster_command_queue = Queue()
        clock_command_queue = Queue()

        soundengine_process = Process(
            target=soundengine.start,
            args=(stop_event, monster_command_queue, clock_command_queue, 80),
        )
        soundengine_process.start()

        self.monster_images: dict[Type[Monster], str] = {
            EtherealEcho: "#ethereal_button"
        }

        self.ui = UI(clock_command_queue, self.monster_images)

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
