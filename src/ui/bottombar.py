from multiprocessing import Queue
from typing import Type

import pygame
import pygame_gui

from src.commands import UpdateClockBpmCommand
from src.config import Configs
from src.field import MonsterField
from src.monsters import Monster
from src.monsters.draggable import DraggableMonster, DraggableMonsterObserver
from src.monsters.monsterinfo import MonsterInfo
from src.ui.components import TextEntryWithCallback


class BottomBar(DraggableMonsterObserver):
    def __init__(
        self,
        ui_manager: pygame_gui.UIManager,
        monster_field: MonsterField,
        clock_command_queue: Queue,
        monster_info: dict[Type[Monster], MonsterInfo],
    ):
        configs = Configs()

        self.ui_manager = ui_manager
        self.clock_command_queue = clock_command_queue
        self.monster_field = monster_field

        rect = pygame.Rect(0, 0, configs.screen_width + 4, 100)
        rect.bottomleft = (-2, 2)
        self.bottom_bar = pygame_gui.elements.UIPanel(
            relative_rect=rect,
            starting_height=0,
            manager=self.ui_manager,
            object_id="#bottom_bar",
            anchors={"left": "left", "bottom": "bottom"},
        )
        self.bpm_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, 100, 100),
            starting_height=0,
            manager=self.ui_manager,
            container=self.bottom_bar,
            object_id="#bpm_container",
        )
        self.bpm_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0, 0, 100, 50),
            text="BPM",
            manager=self.ui_manager,
            container=self.bpm_container,
            object_id="#bpm_label",
        )
        text_rect = pygame.Rect(10, 0, 80, 40)
        self.bpm_textbox = TextEntryWithCallback(
            callback=self.process_bpm,
            relative_rect=text_rect,
            manager=self.ui_manager,
            container=self.bpm_container,
            object_id="#bpm_textbox",
            initial_text="80",
            anchors={"top_target": self.bpm_label},
        )
        self.bpm_textbox.set_allowed_characters(
            ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
        )

        self.monster_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, configs.screen_width - 100, 100),
            starting_height=0,
            manager=self.ui_manager,
            container=self.bottom_bar,
            object_id="#monster_container",
            anchors={"left_target": self.bpm_container},
        )

        self.buttons: list[pygame_gui.elements.UIButton] = []
        self.monster_info = monster_info
        left = 0
        for info in monster_info.values():
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(5 + left, 5, 60, 90),
                text="",
                manager=self.ui_manager,
                container=self.monster_container,
                object_id=info.button_id,
                anchors={"left": "left", "top": "top"},
            )
            button.set_tooltip(
                text=f"<font face=monogram color=normal_text pixel_size=24>"
                f"{info.name}</font>"
                f"<font face=monogram color=normal_text pixel_size=20><br>{info.description}"
                "</font>",
                delay=0.0,
                wrap_width=300,
            )
            self.buttons.append(button)
            left += 65

        self.draggableMonster = None

    def process_events(self, event: pygame.event.Event):
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == self.bpm_textbox:
                self.bpm_textbox.callback()
        elif event.type == pygame_gui.UI_BUTTON_START_PRESS:
            for idx, button in enumerate(self.buttons):
                if button == event.ui_element:
                    self.process_monster_click(
                        list(self.monster_info.keys())[idx],
                        list(self.monster_info.values())[idx],
                    )
                    break

        if self.draggableMonster:
            self.draggableMonster.process_events(event)

    def process_monster_click(
        self, monster_type: Type[Monster], monster_info: MonsterInfo
    ):
        monster = DraggableMonster(
            monster_type=monster_type,
            monster_image=monster_info.image,
            monster_inactive_image=monster_info.inactive_image,
            initial_position=pygame.mouse.get_pos(),
        )
        monster.start_dragging()
        monster.register_observer(self)
        self.draggableMonster = monster

    def update(self, dt: float):
        if self.draggableMonster:
            self.draggableMonster.update(dt)

    def render(self, surface: pygame.Surface):
        if self.draggableMonster:
            self.draggableMonster.render(surface)

    def on_dragging_started(self, monster: DraggableMonster):
        pass

    def on_dragging_stopped(self, monster: DraggableMonster):
        if self.bottom_bar.get_abs_rect().collidepoint(monster.position):
            self.draggableMonster = None
            return

        monster.unregister_observer(self)
        self.monster_field.add_monster(monster)
        self.draggableMonster = None
        pass

    def process_bpm(self):
        bpm = self.bpm_textbox.get_text()
        try:
            bpm = float(bpm)
        except ValueError:
            bpm = 80
            self.bpm_textbox.set_text(str(bpm))

        self.clock_command_queue.put(UpdateClockBpmCommand(bpm))
