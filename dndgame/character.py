from __future__ import annotations

from typing import Dict

from dndgame.dice import roll


RACIAL_BONUSES: dict[str, dict[str, int]] = {
    "Dwarf": {"CON": 2},
    "Elf": {"DEX": 2},
    "Human": {
        "STR": 1,
        "DEX": 1,
        "CON": 1,
        "INT": 1,
        "WIS": 1,
        "CHA": 1,
    },
    "Tiefling": {"CHA": 2, "INT": 1},
}


class Character:
    """Represent a playable character in the game.

    Attributes:
        name: Character's display name.
        race: Character race used to apply racial bonuses.
        stats: Mapping of ability score names to their current values.
        base_hp: Base hit points before racial and constitution modifiers.
        hp: Current hit points.
        max_hp: Maximum hit points.
        level: Character level.
        armor_class: Armor class used for combat.
    """

    def __init__(self, name: str, race: str, base_hp: int) -> None:
        """Initialize a character with basic state.

        Args:
            name: The character's name.
            race: The character's race.
            base_hp: The character's base hit point value.
        """
        self.name: str = name
        self.race: str = race
        self.stats: Dict[str, int] = {}
        self.base_hp: int = base_hp
        self.hp: int = 0
        self.max_hp: int = 0
        self.level: int = 1
        self.armor_class: int = 10

    def get_modifier(self, stat: str) -> int:
        """Calculate the modifier for a named ability score.

        Args:
            stat: The ability score name, such as "STR" or "CON".

        Returns:
            The ability modifier derived from the score.
        """
        return (self.stats[stat] - 10) // 2

    def roll_stats(self) -> None:
        """Roll ability scores and initialize hit points.

        The character receives six ability score rolls and then computes
        hit points using the Constitution modifier and base HP.
        """
        print("Rolling stats...\n")
        stats = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
        for stat in stats:
            print(f"Rolling {stat}...")
            self.stats[stat] = roll(6, 3)

        self.max_hp = self.base_hp + self.get_modifier("CON")
        self.hp = self.max_hp

    def apply_racial_bonuses(self) -> None:
        """Apply racial bonuses to the character's ability scores.

        The bonus mapping is looked up by race name and applied generically
        to each listed ability score.
        """
        bonuses = RACIAL_BONUSES.get(self.race)
        if bonuses is None:
            return

        for stat, bonus in bonuses.items():
            self.stats[stat] += bonus
