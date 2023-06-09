from abc import ABC, abstractmethod
from typing import Callable, Type

from src.clock import Clock
from src.monsters import Monster


class MonsterCommand(ABC):
    """A command that can be executed on a monster dictionary.

    Used to synchronize monsters between the GUI and the sound engine.
    """

    @abstractmethod
    def __init__(self, id: int):
        self.id = id

    @abstractmethod
    def execute(self, monster_dict: dict[int, Monster]) -> Monster:
        pass


class CreateMonsterCommand(MonsterCommand):
    """A command that creates a monster.

    Attributes
    ----------
    id : int
        The ID of the monster.
    """

    def __init__(self, id: int, monster_type: Type[Monster], position: tuple[int, int]):
        super().__init__(id)
        self.monster_type = monster_type
        self.position = position

    def execute(self, monster_dict: dict[int, Monster]):
        print(
            f"Creating monster {self.id} of type {self.monster_type} at position {self.position}"
        )
        monster_dict[self.id] = self.monster_type(self.position)


class DeleteMonsterCommand(MonsterCommand):
    """A command that deletes a monster.

    Attributes
    ----------
    id : int
        The ID of the monster.
    """

    def __init__(self, id: int):
        super().__init__(id)

    def execute(self, monster_dict: dict[int, Monster]):
        del monster_dict[self.id]


class UpdateMonsterPositionCommand(MonsterCommand):
    """A command that updates the position of a monster.

    Attributes
    ----------
    id : int
        The ID of the monster.
    position : tuple[float, float]
        The new position of the monster.
    """

    def __init__(self, id: int, position: tuple[int, int]):
        super().__init__(id)
        self.position = position

    def execute(self, monster_dict: dict[int, Monster]):
        monster_dict[self.id].change_position(self.position)


class UpdateMonsterMutedCommand(MonsterCommand):
    """A command that updates the muted state of a monster.

    Attributes
    ----------
    id : int
        The ID of the monster.
    muted : bool
        Whether the monster is muted or not.
    """

    def __init__(self, id: int, muted: bool):
        super().__init__(id)
        self.muted = muted

    def execute(self, monster_dict: dict[int, Monster]):
        monster_dict[self.id].muted = self.muted


class UpdateMonsterPluginParameterCommand(MonsterCommand):
    """A command that updates a plugin parameter of a monster.

    Attributes
    ----------
    id : int
        The ID of the monster.
    parameter_index : int
        The index of the plugin parameter.
    value : float
        The new value of the plugin parameter.
    """

    def __init__(self, id: int, parameter_index: int, value: float):
        super().__init__(id)
        self.parameter_index = parameter_index
        self.value = value

    def execute(self, monster_dict: dict[int, Monster]):
        monster_dict[self.id].plugin_parameters[self.parameter_index].save(self.value)


class ClockCommand(ABC):
    """A command that can be executed on a clock.

    Used to synchronize clocks between the GUI and the sound engine.
    """

    @abstractmethod
    def execute(self, clock: Clock):
        pass


class UpdateClockBpmCommand(ClockCommand):
    """A command that updates the BPM of a clock.

    Attributes
    ----------
    bpm : float
        The new BPM of the clock.
    """

    def __init__(self, bpm: float):
        self.bpm = bpm

    def execute(self, clock: Clock):
        clock.change_bpm(self.bpm)


class UpdateClockSignatureCommand(ClockCommand):
    """A command that updates the time signature of a clock.

    Attributes
    ----------
    nominator : int
        The new nominator of the time signature.
    denominator : int
        The new denominator of the time signature.
    """

    def __init__(self, nominator: int, denominator: int):
        self.nominator = nominator
        self.denominator = denominator

    def execute(self, clock: Clock):
        clock.change_signature(self.nominator, self.denominator)
