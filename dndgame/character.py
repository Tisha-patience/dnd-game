from __future__ import annotations

from typing import Dict

from dndgame.dice import roll
from dndgame.spells import SpellBook

from .entity import Entity


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


class Character(Entity):
    """Represent a playable character in the game.

    Attributes:
        
        race: Character race used to apply racial bonuses.
        
        level: Character level.
        armor_class: Armor class used for combat.
    """

    def __init__(self, name: str, race: str, base_hp: int) -> None:
        """Initialize a character with basic state.

        Args:

            race: The character's race.
            base_hp: The character's base hit point value.
        """
        super().__init__(name, base_hp)
        self.race: str = race
        self.level: int = 1
        self.spellbook: SpellBook = SpellBook()
        self.xp: int = 0
        self.xp_to_next_level: int = 100

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
        bonuses = RACIAL_BONUSES.get(self.race, {})
        self.stats = {
            stat: value + bonuses.get(stat, 0)
            for stat, value in self.stats.items()
        }

    def gain_xp(self, amount: int) -> None:
        """Award XP and level up if the threshold is reached.

        Args:
            amount: The amount of XP to award.
        """
        self.xp += amount
        if self.xp >= self.xp_to_next_level:
            self.level += 1
            self.max_hp += 5
            self.hp = self.max_hp
            self.xp -= self.xp_to_next_level
            self.xp_to_next_level += 50
            print(f"Level up! {self.name} is now level {self.level}.")
