from asyncio import Queue
from typing import Type

import pygame
import pygame_gui

from src.commands import MonsterCommand
from src.config import Configs
from src.monsters import Monster
from src.monsters.monsterinfo import MonsterInfo


class SideBar:
    def __init__(
        self,
        ui_manager: pygame_gui.UIManager,
        monster_command_queue: "Queue[MonsterCommand]",
        monster_info: dict[Type[Monster], MonsterInfo],
    ):
        configs = Configs()
        self.ui_manager = ui_manager
        self.monster_command_queue = monster_command_queue

        self.sidebar = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(-250, 0, 250, configs.screen_height),
            starting_height=2,
            manager=self.ui_manager,
            object_id="#sidebar",
            anchors={"right": "right", "top": "top"},
            # visible=False,
        )

        self.overlay = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                0, 0, configs.screen_width, configs.screen_height
            ),
            starting_height=1,
            manager=self.ui_manager,
            object_id="#overlay",
            anchors={"left": "left", "top": "top"},
            # visible=False,
        )

        self.side_header = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, 250, 50),
            starting_height=0,
            manager=self.ui_manager,
            container=self.sidebar,
            object_id="#side_header",
        )

        self.side_header_return_arrow = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(0, 0, 50, 50),
            text="",
            manager=self.ui_manager,
            container=self.side_header,
            object_id="#side_header_return_arrow",
        )

        self.side_header_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(15, 0, 200, 50),
            text="Monster Ugly",
            manager=self.ui_manager,
            container=self.side_header,
            object_id="#side_header_label",
            anchors={"left_target": self.side_header_return_arrow},
        )
