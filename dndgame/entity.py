from __future__ import annotations

from typing import Dict

from dndgame.weapon import Weapon


class Entity:
    """Base class for anything that can participate in combat."""

    def __init__(self, name: str, base_hp: int) -> None:
        self.name = name
        self.base_hp = base_hp
        self.hp = base_hp
        self.max_hp = base_hp
        self.armor_class = 10
        self.stats: Dict[str, int] = {}
        self.weapon: Weapon = Weapon("Fists", 4)

    def get_modifier(self, stat: str) -> int:
        return (self.stats[stat] - 10) // 2

    def is_alive(self) -> bool:
        return self.hp > 0