from multiprocessing import Queue

import pygame

from src.commands import CreateMonsterCommand, MonsterCommand
from src.config import Configs
from src.monsters.draggable import DraggableMonster
from src.monsters.monsterrepository import MonsterRepository
from src.soundengine.sound import MonsterSoundEvent


class FieldDraggableMonster:
    def __init__(self, draggable_monster: DraggableMonster, monster_id: int):
        self.draggable_monster = draggable_monster
        self.monster_id = monster_id


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
        monster_id = self.monsters.add_monster(draggable_monster.monster)
        self.draggable_monsters[monster_id] = draggable_monster
        self.monster_command_queue.put(
            CreateMonsterCommand(
                monster_id,
                type(draggable_monster.monster),
                (
                    draggable_monster.position[0] / self.width,
                    draggable_monster.position[1] / self.height,
                ),
            )
        )
        print("Added monster", monster_id)
        draggable_monster.register_observer(self)

    def on_dragging_started(self, draggable_monster: DraggableMonster):
        pass

    def on_dragging_stopped(self, draggable_monster: DraggableMonster):
        pass
