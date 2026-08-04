from __future__ import annotations

from dndgame.character import Character
from dndgame.dice import roll


class Combat:
    """Manage a combat encounter between two characters.

    Attributes:
        player: The player's character.
        enemy: The opposing character.
        round: The current combat round number.
        initiative_order: Turn order determined by initiative rolls.
    """

    def __init__(self, player: Character, enemy: Character) -> None:
        """Initialize a combat encounter.

        Args:
            player: The player's character.
            enemy: The opposing character.
        """
        self.player: Character = player
        self.enemy: Character = enemy
        self.round: int = 0
        self.initiative_order: list[Character] = []

    def roll_initiative(self) -> list[Character]:
        """Roll initiative for combat order.

        Both combatants roll a d20 plus their DEX modifier. The higher
        roll acts first.

        Returns:
            The combatants in turn order, highest initiative first.
        """
        player_init = roll(20, 1) + self.player.get_modifier("DEX")
        enemy_init = roll(20, 1) + self.enemy.get_modifier("DEX")

        if player_init >= enemy_init:
            self.initiative_order = [self.player, self.enemy]
        else:
            self.initiative_order = [self.enemy, self.player]

        return self.initiative_order

    def attack(self, attacker: Character, defender: Character) -> int:
        """Resolve one attack from attacker against defender.

        Rolls a d20 plus the attacker's STR modifier against the
        defender's armor class. On a hit, rolls weapon damage and
        applies it to the defender's HP.

        Args:
            attacker: The character making the attack.
            defender: The character being attacked.

        Returns:
            The amount of damage dealt, or 0 if the attack missed.
        """
        attack_roll = roll(20, 1) + attacker.get_modifier("STR")
        weapon_max_damage = 6
        if attack_roll >= defender.armor_class:
            damage = roll(weapon_max_damage, 1)
            defender.hp -= damage
            return damage
        return 0