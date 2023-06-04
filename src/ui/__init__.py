from multiprocessing import Queue
from typing import Type

import pygame
import pygame_gui

from src.config import Configs
from src.field import MonsterField
from src.monsters import Monster
from src.monsters.monsterinfo import MonsterInfo
from src.ui.bottombar import BottomBar
from src.ui.sidebar import SideBar


class UI:
    def __init__(
        self,
        monster_field: MonsterField,
        clock_command_queue: Queue,
        monster_command_queue: Queue,
        monster_info: dict[Type[Monster], MonsterInfo],
    ) -> None:
        configs = Configs()
        self.manager = pygame_gui.UIManager(
            (configs.screen_width, configs.screen_height),
        )
        self.manager.add_font_paths("monogram", "resources/fonts/monogram.ttf")
        self.manager.preload_fonts(
            [{"name": "monogram", "point_size": 32, "style": "regular"}],
        )
        self.manager.preload_fonts(
            [{"name": "monogram", "point_size": 24, "style": "regular"}],
        )
        self.manager.preload_fonts(
            [{"name": "monogram", "point_size": 16, "style": "regular"}],
        )
        self.manager.get_theme().load_theme("resources/configs/theme.json")

        self.bottom_bar = BottomBar(
            self.manager, monster_field, clock_command_queue, monster_info
        )
        self.side_bar = SideBar(self.manager, monster_command_queue, monster_info)

    def process_events(self, event: pygame.event.Event):
        self.manager.process_events(event)
        self.bottom_bar.process_events(event)

    def update(self, delta_time: float):
        self.manager.update(delta_time / 1000)
        self.bottom_bar.update(delta_time)

    def render(self, screen: pygame.Surface):
        self.manager.draw_ui(screen)
        self.bottom_bar.render(screen)
