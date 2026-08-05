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


def test_apply_racial_bonuses_supports_new_race_mapping() -> None:
    """A race added to the bonus mapping should apply its bonuses automatically."""
    character = Character("Mira", "Tiefling", 10)
    character.stats = {
        "STR": 10,
        "DEX": 10,
        "CON": 10,
        "INT": 10,
        "WIS": 10,
        "CHA": 10,
    }

    character.apply_racial_bonuses()

    assert character.stats["CHA"] == 12
    assert character.stats["INT"] == 11


def test_gain_xp_below_threshold_does_not_level_up() -> None:
    """Gaining XP below the threshold should not trigger a level up."""
    character = Character("Hero", "Human", 10)
    character.max_hp = character.hp = 10

    character.gain_xp(30)

    assert character.xp == 30
    assert character.level == 1
    assert character.max_hp == 10
    assert character.hp == 10


def test_gain_xp_at_threshold_levels_up_and_heals() -> None:
    """Reaching the XP threshold should level up, boost max HP, and heal."""
    character = Character("Hero", "Human", 10)
    character.max_hp = 10
    character.hp = 4  # simulate a damaged character before leveling up

    character.gain_xp(100)

    assert character.level == 2
    assert character.max_hp == 15
    assert character.hp == 15
    assert character.xp == 0
    assert character.xp_to_next_level == 150