from asyncio import Queue
from typing import Type

import pygame
import pygame_gui
from pygame_gui.core import IContainerLikeInterface

from src.commands import (
    DeleteMonsterCommand,
    MonsterCommand,
    UpdateMonsterMutedCommand,
    UpdateMonsterPluginParameterCommand,
)
from src.config import Configs
from src.field import MonsterField
from src.monsters import Monster
from src.monsters.monsterinfo import MonsterInfo


class Parameter:
    def __init__(
        self,
        id: int,
        name: str,
        value: float,
        min: float,
        max: float,
        step: float,
        container: IContainerLikeInterface,
        top: int,
        manager: pygame_gui.UIManager,
        side_bar: "SideBar",
    ):
        self.id = id
        self.name = name
        self.value = value
        self.min = min
        self.max = max
        self.step = step
        self.side_bar = side_bar

        self.label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(15, top, 250, 40),
            text=name,
            manager=manager,
            container=container,
            anchors={"left": "left", "top": "top"},
        )

        self.slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(15, top + 40, 210, 40),
            start_value=value,
            value_range=(float(min), float(max)),
            manager=manager,
            container=container,
            anchors={"left": "left", "top": "top"},
            click_increment=step,
        )

    def kill(self):
        self.label.kill()
        self.slider.kill()

    def process_events(self, event: pygame.event.Event):
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.slider:
                # enforce step
                old_value = self.value
                self.value = round(event.value / self.step) * self.step
                self.slider.set_current_value(self.value)

                if old_value != self.value:
                    self.side_bar.update_parameter(self)


class SideBar:
    def __init__(
        self,
        ui_manager: pygame_gui.UIManager,
        monster_field: MonsterField,
        monster_command_queue: "Queue[MonsterCommand]",
        monster_info: dict[Type[Monster], MonsterInfo],
    ):
        configs = Configs()
        self.ui_manager = ui_manager
        self.monster_command_queue = monster_command_queue
        self.monster_info = monster_info
        self.current_monster: Monster = None
        self.current_monster_id: int = None
        self.monster_field = monster_field

        self.sidebar = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(-260, 0, 260, configs.screen_height),
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
            relative_rect=pygame.Rect(0, 0, 260, 50),
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

        self.remove_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(15, 50, 200, 50),
            text="Remove",
            manager=self.ui_manager,
            container=self.sidebar,
            object_id="#remove_label",
            anchors={"left": "left", "top": "top"},
        )

        self.remove_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(210, 50, 50, 50),
            text="",
            manager=self.ui_manager,
            container=self.sidebar,
            object_id="#remove_button",
            anchors={"left": "left", "top": "top"},
        )

        self.mute_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(15, 100, 200, 50),
            text="Mute",
            manager=self.ui_manager,
            container=self.sidebar,
            object_id="#mute_label",
            anchors={"left": "left", "top": "top"},
        )

        self.mute_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(210, 100, 50, 50),
            text="",
            manager=self.ui_manager,
            container=self.sidebar,
            object_id="#mute_button",
            anchors={"left": "left", "top": "top"},
        )

        self.unmute_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(210, 100, 50, 50),
            text="",
            manager=self.ui_manager,
            container=self.sidebar,
            object_id="#unmute_button",
            anchors={"left": "left", "top": "top"},
            visible=False,
        )

        self.parameters: list[Parameter] = []

        self.parameter_container = pygame_gui.elements.UIScrollingContainer(
            relative_rect=pygame.Rect(0, 150, 255, configs.screen_height - 50),
            manager=self.ui_manager,
            container=self.sidebar,
            object_id="#parameter_container",
        )

    def process_events(self, event: pygame.event.Event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.side_header_return_arrow:
                self.hide()
            elif event.ui_element == self.mute_button:
                self.monster_command_queue.put(
                    UpdateMonsterMutedCommand(
                        self.current_monster_id,
                        True,
                    )
                )
                self.current_monster.mute()
                self.show_unmute()
            elif event.ui_element == self.unmute_button:
                self.monster_command_queue.put(
                    UpdateMonsterMutedCommand(
                        self.current_monster_id,
                        False,
                    )
                )
                self.current_monster.unmute()
                self.show_mute()
            elif event.ui_element == self.remove_button:
                self.monster_command_queue.put(
                    DeleteMonsterCommand(self.current_monster_id)
                )
                self.monster_field.remove_monster(self.current_monster_id)
                self.hide()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if not self.sidebar.get_abs_rect().collidepoint(event.pos):
                    self.hide()

        for parameter in self.parameters:
            parameter.process_events(event)

    def update_parameter(self, parameter: Parameter):
        self.monster_command_queue.put(
            UpdateMonsterPluginParameterCommand(
                self.current_monster_id,
                parameter.id,
                parameter.value,
            )
        )
        self.current_monster.plugin_parameters[parameter.id].save(parameter.value)

    def show_mute(self):
        self.mute_label.set_text("Mute")
        self.unmute_button.hide()
        self.unmute_button.set_dimensions((0, 0))
        self.mute_button.show()
        self.mute_button.set_dimensions((50, 50))

    def show_unmute(self):
        self.mute_label.set_text("Unmute")
        self.mute_button.hide()
        self.mute_button.set_dimensions((0, 0))
        self.unmute_button.show()
        self.unmute_button.set_dimensions((50, 50))

    def show(self, monster: Monster, monster_id: int):
        monster_info = self.monster_info[type(monster)]
        configs = Configs()
        self.current_monster = monster
        self.current_monster_id = monster_id

        self.side_header_label.set_text(monster_info.name)

        for parameter in self.parameters:
            parameter.kill()

        self.parameters = []

        for idx, parameter in enumerate(monster.plugin_parameters):
            self.parameters.append(
                Parameter(
                    idx,
                    parameter.name,
                    parameter.value(),
                    parameter.min,
                    parameter.max,
                    parameter.step,
                    self.parameter_container,
                    len(self.parameters) * 80,
                    self.ui_manager,
                    self,
                )
            )
        self.parameter_container.set_scrollable_area_dimensions(
            (230, max(len(self.parameters) * 80 + 50, configs.screen_height - 50))
        )

        if monster.muted:
            self.show_unmute()
        else:
            self.show_mute()

        self.sidebar.show()
        self.overlay.show()

    def hide(self):
        self.sidebar.hide()
        self.overlay.hide()
