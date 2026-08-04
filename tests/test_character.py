from unittest.mock import patch

from dndgame.character import Character


def test_roll_stats_initializes_ability_scores_and_hp() -> None:
    """Rolling stats should populate ability scores and set HP."""
    with patch("dndgame.character.roll", side_effect=[10, 12, 14, 8, 11, 15]):
        character = Character("Gimli", "Dwarf", 12)
        character.roll_stats()

    assert character.stats["STR"] == 10
    assert character.stats["DEX"] == 12
    assert character.stats["CON"] == 14
    assert character.max_hp == 14
    assert character.hp == 14


def test_apply_racial_bonuses_updates_the_expected_stats() -> None:
    """Elf and Dwarf bonuses should modify the correct ability scores."""
    character = Character("Lia", "Elf", 10)
    character.stats = {
        "STR": 10,
        "DEX": 10,
        "CON": 10,
        "INT": 10,
        "WIS": 10,
        "CHA": 10,
    }

    character.apply_racial_bonuses()

    assert character.stats["DEX"] == 12
