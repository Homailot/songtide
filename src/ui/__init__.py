import pygame
import pygame_gui

from src.config import Configs
from src.ui.bottombar import BottomBar


class UI:
    def __init__(self) -> None:
        configs = Configs()
        self.manager = pygame_gui.UIManager(
            (configs.screen_width, configs.screen_height),
        )
        self.manager.add_font_paths("monogram", "resources/fonts/monogram.ttf")
        self.manager.preload_fonts([
            {
                "name": "monogram",
                "point_size": 32,
                "style": "regular"
            }
        ])
        self.manager.get_theme().load_theme("resources/configs/theme.json")

        self.bottom_bar = BottomBar(self.manager)
    
    def process_events(self, event: pygame.event.Event):
        self.manager.process_events(event)

    def update(self, delta_time: float):
        self.manager.update(delta_time / 1000)

    def render(self, screen: pygame.Surface):
        self.manager.draw_ui(screen)
