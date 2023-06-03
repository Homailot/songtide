import pygame
import pygame_gui

from src.config import Configs


class UI:
    def __init__(self) -> None:
        configs = Configs()
        self.manager = pygame_gui.UIManager(
            (configs.screen_width, configs.screen_height)
        )
        self.button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 275), (100, 50)),
            text="Click me",
            manager=self.manager,
        )

    def process_events(self, event: pygame.event.Event):
        self.manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.button:
                print("Button pressed!")

    def update(self, delta_time: float):
        self.manager.update(delta_time / 1000)

    def render(self, screen: pygame.Surface):
        self.manager.draw_ui(screen)
