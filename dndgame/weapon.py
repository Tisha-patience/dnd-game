from __future__ import annotations


class Weapon:
    """Represent a physical weapon used for damage rolls.

    Attributes:
        name: The weapon's name.
        damage_die: The number of sides on the die rolled for damage.
    """

    def __init__(self, name: str, damage_die: int) -> None:
        """Initialize a weapon.

        Args:
            name: The weapon's name.
            damage_die: The number of sides on the damage die.
        """
        self.name = name
        self.damage_die = damage_die
