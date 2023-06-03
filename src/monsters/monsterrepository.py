from src.monsters import Monster


class MonsterRepository:
    monsters: dict[int, Monster]
    monster_id_counter: int

    def __init__(self):
        self.monsters = {}
        self.monster_id_counter = 0

    def add_monster(self, monster: Monster) -> int:
        """Adds a monster to the repository.

        Parameters
        ----------
        monster : Monster
            The monster to add.
        """
        self.monsters[self.monster_id_counter] = monster
        return_value = self.monster_id_counter

        self.monster_id_counter += 1
        return return_value

    def remove_monster(self, monster_id: int) -> None:
        """Removes a monster from the repository.

        Parameters
        ----------
        monster_id : int
            The ID of the monster to remove.
        """
        del self.monsters[monster_id]

    def get_monster(self, monster_id: int) -> Monster:
        """Gets a monster from the repository.

        Parameters
        ----------
        monster_id : int
            The ID of the monster to get.

        Returns
        -------
        Monster
            The monster.
        """
        return self.monsters[monster_id]

    
