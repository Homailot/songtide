from multiprocessing import Queue

import pygame
import pygame_gui

from src.commands import UpdateClockBpmCommand
from src.config import Configs
from src.ui.components import TextEntryWithCallback


class BottomBar:
    def __init__(self, ui_manager: pygame_gui.UIManager, clock_command_queue: Queue):
        configs = Configs()

        self.ui_manager = ui_manager

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
            callback=lambda: self.process_bpm(),
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
        self.clock_command_queue = clock_command_queue

    def process_events(self, event: pygame.event.Event):
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            self.bpm_textbox.callback()

    def process_bpm(self):
        bpm = self.bpm_textbox.get_text()
        try:
            bpm = float(bpm)
        except ValueError:
            bpm = 80
            self.bpm_textbox.set_text(str(bpm))

        self.clock_command_queue.put(UpdateClockBpmCommand(bpm))
