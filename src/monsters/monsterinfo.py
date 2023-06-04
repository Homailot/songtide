import pygame


class MonsterInfo:
    def __init__(
        self, name: str, description: str, button_id: str, image: pygame.Surface
    ) -> None:
        self.name = name
        self.description = description
        self.button_id = button_id
        self.image = image
