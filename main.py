from __future__ import annotations

from typing import Any

from dndgame.character import Character, RACIAL_BONUSES
from dndgame.dice import roll


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
        bonus_text = ", ".join(f"+{amount} {stat}" for stat, amount in bonuses.items())
        print(f"{index}. {race_name} ({bonus_text})")

    race_choice = prompt_menu_choice(
        "Enter choice (1-{}): ".format(len(RACIAL_BONUSES)),
        len(RACIAL_BONUSES),
    )
    print("\n")
    race_names = list(RACIAL_BONUSES)
    race = race_names[race_choice - 1]

    character = Character(name, race, 10)
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


def simple_combat(player: Character) -> bool:
    """Run a simple combat loop against a goblin.

    Args:
        player: The player's character.

    Returns:
        True if the player defeats the goblin, False if they flee.
    """
    print("\nA goblin appears!")
    goblin_hp = 5

    while goblin_hp > 0:
        print(f"\nGoblin HP: {goblin_hp}")
        print("\nYour turn!")
        print("1. Attack")
        print("2. Run away")
        print()

        choice = prompt_menu_choice("What do you do? ", 2)
        if choice == 1:
            attack = roll(20, 1)
            if attack >= 10:
                damage = roll(4, 1)
                goblin_hp -= damage
                print(f"You hit for {damage} damage!")
            else:
                print("You missed!")
        elif choice == 2:
            return False

    return True


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
            victory = simple_combat(player)
            if victory:
                print("You defeated the goblin!")
            else:
                print("You ran away!")
        elif choice == 2:
            display_character(player)
        elif choice == 3:
            break


if __name__ == "__main__":
    main()
