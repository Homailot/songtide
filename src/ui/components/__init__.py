from typing import Callable, Dict, Optional, Tuple, Union

import pygame
import pygame_gui
from pygame_gui.core import ObjectID, UIElement
from pygame_gui.core.interfaces import IContainerLikeInterface, IUIManagerInterface


class TextEntryWithCallback(pygame_gui.elements.UITextEntryLine):
    def __init__(
        self,
        callback: Callable[[], None],
        relative_rect: pygame.Rect | Tuple[int, int, int, int],
        manager: IUIManagerInterface | None = None,
        container: IContainerLikeInterface | None = None,
        parent_element: UIElement | None = None,
        object_id: ObjectID | str | None = None,
        anchors: Dict[str, str | UIElement] | None = None,
        visible: int = 1,
        *,
        initial_text: str | None = None,
        placeholder_text: str | None = None
    ):
        super().__init__(
            relative_rect,
            manager,
            container,
            parent_element,
            object_id,
            anchors,
            visible,
            initial_text=initial_text,
            placeholder_text=placeholder_text,
        )

        self.callback = callback

    def unfocus(self):
        super().unfocus()

        self.callback()
