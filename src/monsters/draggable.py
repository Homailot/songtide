from abc import ABC, abstractmethod

import pygame

from src.monsters import Monster


class DraggableMonster:
    def __init__(
        self,
        monster: Monster,
        monster_image: pygame.Surface,
        initial_position: tuple[int, int],
    ) -> None:
        self.monster = monster
        self.monster_image = monster_image
        self.position = initial_position
        self.dragging = False
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def unregister_observer(self, observer):
        self.observers.remove(observer)

    def start_dragging(self):
        for observer in self.observers:
            observer.on_dragging_started(self)
        self.dragging = True

    def stop_dragging(self):
        for observer in self.observers:
            observer.on_dragging_stopped(self)
        self.dragging = False

    def process_events(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                mouse_position = pygame.mouse.get_pos()
                if (
                    mouse_position[0] >= self.position[0]
                    and mouse_position[0]
                    <= self.position[0] + self.monster_image.get_width()
                    and mouse_position[1] >= self.position[1]
                    and mouse_position[1]
                    <= self.position[1] + self.monster_image.get_height()
                ):
                    self.start_dragging()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                self.stop_dragging()

    def update(self, delta_time: float):
        if self.dragging:
            mouse_position = pygame.mouse.get_pos()
            self.position = (
                mouse_position[0] - self.monster_image.get_width() / 2,
                mouse_position[1] - self.monster_image.get_height() / 2,
            )

    def render(self, screen: pygame.Surface):
        screen.blit(self.monster_image, self.position)


class DraggableMonsterObserver(ABC):
    @abstractmethod
    def on_dragging_started(self, draggable_monster: DraggableMonster):
        pass

    @abstractmethod
    def on_dragging_stopped(self, draggable_monster: DraggableMonster):
        pass
