from __future__ import annotations

from typing import Any

from dndgame.character import Character, RACIAL_BONUSES
from dndgame.dice import roll
from dndgame.enemy import Enemy
from dndgame.spells import Spell
from dndgame.weapon import Weapon
from dndgame.combat import Combat


def prompt_non_empty_input(prompt: str) -> str:
    """Prompt for non-empty user input.

    Args:
        prompt: The text displayed to the user.

    Returns:
        A non-empty string entered by the user.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value

        print("Please enter a value.")


def prompt_menu_choice(prompt: str, max_choice: int) -> int:
    """Prompt for a menu choice within a valid numeric range.

    Args:
        prompt: The text displayed to the user.
        max_choice: The highest allowed numeric choice.

    Returns:
        A valid menu choice as an integer.
    """
    while True:
        raw_value = input(prompt).strip()
        try:
            choice = int(raw_value)
        except ValueError:
            print("Please enter a number.")
            continue

        if 1 <= choice <= max_choice:
            return choice

        print(f"Please enter a number from 1 to {max_choice}.")


def create_character() -> Character:
    """Create a new character from CLI input.

    Returns:
        A populated Character instance.
    """
    print("Welcome to D&D Adventure!")
    name = prompt_non_empty_input("Enter your character's name: ")

    print("\nChoose your race:")
    for index, race_name in enumerate(RACIAL_BONUSES, start=1):
        bonuses = RACIAL_BONUSES[race_name]
        bonus_text = ", ".join(
            map(lambda pair: f"+{pair[1]} {pair[0]}", bonuses.items())
        )
        print(f"{index}. {race_name} ({bonus_text})")

    race_choice = prompt_menu_choice(
        "Enter choice (1-{}): ".format(len(RACIAL_BONUSES)),
        len(RACIAL_BONUSES),
    )
    print("\n")
    race_names = list(RACIAL_BONUSES)
    race = race_names[race_choice - 1]

    character = Character(name, race, 10)
    character.weapon = Weapon("Longsword", 8)
    character.spellbook.add_spell(Spell("Firebolt", 1, "Evocation", 5))
    character.roll_stats()
    character.apply_racial_bonuses()
    return character


def display_character(character: Character) -> None:
    """Display the character's stats and hit points.

    Args:
        character: The character to display.
    """
    print(f"\n{character.name} the {character.race}")
    print("\nStats:")
    for stat, value in character.stats.items():
        modifier = character.get_modifier(stat)
        print(f"{stat}: {value} ({'+' if modifier >= 0 else ''}{modifier})")
    print(f"\nHP: {character.hp}")


def main() -> None:
    """Run the main game loop."""
    player = create_character()

    while True:
        print("\nWhat would you like to do?")
        print("1. Fight a goblin")
        print("2. View character")
        print("3. Quit")

        choice = prompt_menu_choice("Enter choice (1-3): ", 3)

        if choice == 1:
            enemy = Enemy("Goblin", 5, xp_value=10)
            # You can optionally pass DungeonMaster() here once you have an OPENAI_API_KEY configured.
            combat = Combat(player, enemy)
            victory = combat.start()
            if victory:
                print("You defeated the goblin!")
            elif player.is_alive():
                print("You ran away!")
            else:
                print("Game Over!")
            break


if __name__ == "__main__":
    main()
