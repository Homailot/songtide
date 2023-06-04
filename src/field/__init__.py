from multiprocessing import Queue

import pygame

from src.commands import (
    CreateMonsterCommand,
    MonsterCommand,
    UpdateMonsterPositionCommand,
)
from src.config import Configs
from src.monsters.draggable import DraggableMonster
from src.monsters.monsterrepository import MonsterRepository
from src.soundengine.sound import MonsterSoundEvent


class MonsterField:
    def __init__(
        self,
        monster_command_queue: "Queue[MonsterCommand]",
        monster_sound_queue: "Queue[MonsterSoundEvent]",
    ):
        configs = Configs()

        self.monsters = MonsterRepository()
        self.draggable_monsters: dict[int, DraggableMonster] = {}
        self.monster_command_queue = monster_command_queue
        self.monster_sound_queue = monster_sound_queue

        self.width = configs.screen_width
        self.height = configs.screen_height - 100

        self.ui_observer = None

    def register_ui_observer(self, ui_observer):
        self.ui_observer = ui_observer

    def process_events(self, event: pygame.event.Event):
        for field_monster in self.draggable_monsters.values():
            field_monster.process_events(event)

    def update(self, delta_time: float):
        while not self.monster_sound_queue.empty():
            sound_event = self.monster_sound_queue.get()
            if sound_event.monster_id in self.draggable_monsters:
                self.draggable_monsters[sound_event.monster_id].set_active(
                    sound_event.on
                )

        for field_monster in self.draggable_monsters.values():
            field_monster.update(delta_time)

    def render(self, screen: pygame.Surface):
        for field_monster in self.draggable_monsters.values():
            field_monster.render(screen)

    def add_monster(self, draggable_monster: DraggableMonster):
        monster = draggable_monster.monster_type(draggable_monster.position)
        monster_id = self.monsters.add_monster(monster)
        draggable_monster.set_monster_id(monster_id)
        self.draggable_monsters[monster_id] = draggable_monster
        self.monster_command_queue.put(
            CreateMonsterCommand(
                monster_id,
                draggable_monster.monster_type,
                (
                    draggable_monster.position[0] / self.width,
                    1 - (draggable_monster.position[1] / self.height),
                ),
            )
        )
        print("Added monster", monster_id)
        draggable_monster.register_observer(self)

    def on_dragging_started(self, draggable_monster: DraggableMonster):
        pass

    def on_dragging_stopped(self, draggable_monster: DraggableMonster):
        if draggable_monster.position[1] > self.height:
            draggable_monster.position = draggable_monster.drag_start_position
            return

        self.monster_command_queue.put(
            UpdateMonsterPositionCommand(
                draggable_monster.monster_id,
                (
                    draggable_monster.position[0] / self.width,
                    1 - (draggable_monster.position[1] / self.height),
                ),
            )
        )

    def on_right_click(self, draggable_monster: DraggableMonster):
        if self.ui_observer:
            self.ui_observer.on_monster_right_click(
                self.monsters.get_monster(draggable_monster.monster_id),
                draggable_monster.monster_id,
            )
