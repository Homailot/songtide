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
        self.monster_info = monster_info

        self.sidebar = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(-250, 0, 250, configs.screen_height),
            starting_height=2,
            manager=self.ui_manager,
            object_id="#sidebar",
            anchors={"right": "right", "top": "top"},
            visible=False,
        )

        self.overlay = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                0, 0, configs.screen_width, configs.screen_height
            ),
            starting_height=1,
            manager=self.ui_manager,
            object_id="#overlay",
            anchors={"left": "left", "top": "top"},
            visible=False,
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

    def process_events(self, event: pygame.event.Event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.side_header_return_arrow:
                self.hide()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if not self.sidebar.get_abs_rect().collidepoint(event.pos):
                    self.hide()

    def show(self, monster: Monster):
        self.side_header_label.set_text(self.monster_info[type(monster)].name)
        self.sidebar.show()
        self.overlay.show()

    def hide(self):
        self.sidebar.hide()
        self.overlay.hide()
