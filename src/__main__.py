import sys
from enum import Enum
from multiprocessing import Process, Event, Manager
from soundengine import soundengine

import fluidsynth
import pygame

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

    def render(self, screen: pygame.Surface):
        screen.fill("purple")
        pygame.display.flip()

    def update(self):
        pass

    def handle_run(self, screen: pygame.Surface):
        self.process_events()

        while self.lag >= self.milliseconds_per_frame:
            self.update()
            self.lag -= self.milliseconds_per_frame

        self.render(screen)
        self.delta_time = self.clock.tick(60)
        self.lag += self.delta_time

    def start(self):
        pygame.init()
        screen = pygame.display.set_mode((1280, 700))
        pygame.display.set_caption("Songtide")

        self.clock = pygame.time.Clock()
        self.delta_time = 0.0
        self.lag = 0.0

        self.state = GameState.RUNNING

        with Manager() as manager:
            stop_event = manager.Event()
            soundengine_process = Process(target=soundengine.start, args=(stop_event,))
            soundengine_process.start()

            running = True
            while running:
                match self.state:
                    case GameState.RUNNING:
                        self.handle_run(screen)
                    case GameState.STOPPED:
                        running = False
                    case _:
                        pass

            stop_event.set()
            soundengine_process.join()

            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    fs = fluidsynth.Synth()
    fs.delete()

    game = Game()
    game.start()
