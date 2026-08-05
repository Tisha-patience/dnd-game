from __future__ import annotations

from dndgame.character import Character
from dndgame.entity import Entity
from dndgame.dice import roll


class Combat:
    """Manage a combat encounter between two characters.

    Attributes:
        player: The player's character.
        enemy: The opposing character.
        round: The current combat round number.
        initiative_order: Turn order determined by initiative rolls.
    """

    def __init__(self, player: Character, enemy: Entity) -> None:
        """Initialize a combat encounter.

        Args:
            player: The player's character.
            enemy: The opposing character.
        """
        self.player: Character = player
        self.enemy: Entity = enemy
        self.round: int = 0
        self.initiative_order: list[Entity] = []

    def roll_initiative(self) -> list[Entity]:
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

    def attack(self, attacker: Entity, defender: Entity) -> int:
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
        if attack_roll >= defender.armor_class:
            damage = roll(attacker.weapon.damage_die, 1)
            defender.hp -= damage
            return damage
        return 0

    def start(self) -> bool:
        """Run combat until someone dies or the player flees."""

        print(f"\nA {self.enemy.name} appears!")

        while self.player.is_alive() and self.enemy.is_alive():
            print(f"\n{self.enemy.name} HP: {self.enemy.hp}")
            print(f"{self.player.name} HP: {self.player.hp}")

            print("\n1. Attack")
            print("2. Cast Spell")
            print("3. Run away")

            while True:
                try:
                    choice = int(input("Choice: "))
                except ValueError:
                    print("Please enter a number.")
                    continue

                if choice == 3:
                    return False

                if choice == 2 and not self.player.spellbook.spells:
                    print("You have no spells ready to cast.")
                    continue

                if choice in {1, 2}:
                    break

                print("Please enter a valid choice.")

            if choice == 1:
                damage = self.attack(self.player, self.enemy)
            else:
                spell = self.player.spellbook.spells[0]
                damage = spell.cast(self.player, self.enemy)

            if damage:
                print(f"You hit for {damage} damage!")
            else:
                print("You missed!")

            if not self.enemy.is_alive():
                print(f"{self.enemy.name} was defeated!")
                return True

            damage = self.attack(self.enemy, self.player)

            if damage:
                print(f"{self.enemy.name} hits you for {damage} damage!")
            else:
                print(f"{self.enemy.name} misses!")

            if not self.player.is_alive():
                print("You have been defeated!")
                return False

        return False
