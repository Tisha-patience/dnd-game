from __future__ import annotations

from dndgame.entity import Entity


class Enemy(Entity):
    """Represent an enemy in combat."""

    def __init__(self, name: str, base_hp: int, xp_value: int) -> None:
        super().__init__(name, base_hp)
        self.xp_value: int = xp_value

        self.stats = {
            "STR": 10,
            "DEX": 10,
            "CON": 10,
            "INT": 8,
            "WIS": 8,
            "CHA": 8,
        }