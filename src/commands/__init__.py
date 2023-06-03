from abc import ABC, abstractmethod

from src.clock import Clock
from src.monsters import Monster


class MonsterCommand(ABC):
    """A command that can be executed on a monster dictionary.

    Used to synchronize monsters between the GUI and the sound engine.
    """

    @abstractmethod
    def execute(self, monster_dict: dict[int, Monster]):
        pass


class CreateMonsterCommand(MonsterCommand):
    """A command that creates a monster.

    Attributes
    ----------
    id : int
        The ID of the monster.
    """

    def __init__(self, id: int):
        self.id = id

    def execute(self, monster_dict: dict[int, Monster]):
        monster_dict[self.id] = Monster(self.id)


class DeleteMonsterCommand(MonsterCommand):
    """A command that deletes a monster.

    Attributes
    ----------
    id : int
        The ID of the monster.
    """

    def __init__(self, id: int):
        self.id = id

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
        self.id = id
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
        self.id = id
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
        self.id = id
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
