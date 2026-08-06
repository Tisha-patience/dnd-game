from unittest.mock import patch

from dndgame.character import Character
from dndgame.combat import Combat
from dndgame.enemy import Enemy
from dndgame.spells import Spell

def make_player() -> Character:
    """Build a player Character with fixed, known stats for testing."""
    player = Character("Hero", "Human", 10)
    player.stats = {
        "STR": 14,
        "DEX": 12,
        "CON": 10,
        "INT": 10,
        "WIS": 10,
        "CHA": 10,
    }
    player.hp = player.max_hp = 10
    return player


def make_enemy() -> Enemy:
    """Build an Enemy with fixed, known stats for testing."""
    return Enemy("Goblin", 5, xp_value=10)


def test_attack_hits_and_deals_damage() -> None:
    """A high attack roll against low armor class should deal damage."""
    combat = Combat(make_player(), make_enemy())

    # First roll(20, 1) -> attack roll; second roll(6, 1) -> damage roll.
    with patch("dndgame.combat.roll", side_effect=[15, 4]):
        damage = combat.attack(combat.player, combat.enemy)

    assert damage == 4
    assert combat.enemy.hp == combat.enemy.max_hp - 4


def test_attack_misses_and_deals_no_damage() -> None:
    """A low attack roll against armor class should deal zero damage."""
    combat = Combat(make_player(), make_enemy())
    starting_hp = combat.enemy.hp

    # roll(20, 1) -> low attack roll, misses armor_class of 10.
    with patch("dndgame.combat.roll", return_value=1):
        damage = combat.attack(combat.player, combat.enemy)

    assert damage == 0
    assert combat.enemy.hp == starting_hp


def test_roll_initiative_player_goes_first_on_higher_roll() -> None:
    """The player should act first when their initiative roll is higher."""
    combat = Combat(make_player(), make_enemy())

    # player DEX modifier is +1 (stat 12), enemy DEX modifier is +0 (stat 10)
    # side_effect order matches call order in roll_initiative:
    # first call -> player's d20, second call -> enemy's d20
    with patch("dndgame.combat.roll", side_effect=[10, 5]):
        order = combat.roll_initiative()

    assert order == [combat.player, combat.enemy]


def test_roll_initiative_enemy_goes_first_on_higher_roll() -> None:
    """The enemy should act first when their initiative roll is higher."""
    combat = Combat(make_player(), make_enemy())

    with patch("dndgame.combat.roll", side_effect=[3, 15]):
        order = combat.roll_initiative()

    assert order == [combat.enemy, combat.player]


def test_start_player_wins_in_one_hit() -> None:
    """If the player's first attack kills the enemy, start() returns True."""
    combat = Combat(make_player(), make_enemy())

    with patch("builtins.input", side_effect=["1"]), \
         patch("dndgame.combat.roll", side_effect=[15, 6]):
        result = combat.start()

    assert result is True
    assert combat.enemy.hp <= 0
    assert combat.player.hp == combat.player.max_hp


def test_start_player_loses() -> None:
    """If the enemy's attacks reduce the player to 0 HP, start() returns False."""
    combat = Combat(make_player(), make_enemy())

    with patch("builtins.input", side_effect=["1", "1"]), \
         patch(
             "dndgame.combat.roll",
             side_effect=[5, 15, 6, 5, 15, 6],
         ):
        result = combat.start()

    assert result is False
    assert not combat.player.is_alive()


def test_start_player_runs_away() -> None:
    """Choosing to run away should end combat immediately with no damage."""
    combat = Combat(make_player(), make_enemy())

    with patch("builtins.input", side_effect=["3"]):
        result = combat.start()

    assert result is False
    assert combat.player.hp == combat.player.max_hp
    assert combat.enemy.hp == combat.enemy.max_hp


def test_start_player_casts_spell_and_wins() -> None:
    """If the player's spell kills the enemy, start() returns True."""
    player = make_player()
    player.spellbook.add_spell(Spell("Firebolt", 1, "Evocation", 5))
    combat = Combat(player, make_enemy())

    with patch("builtins.input", side_effect=["2"]):
        result = combat.start()

    assert result is True
    assert combat.enemy.hp <= 0    


def test_start_uses_dungeon_master_narration_when_provided() -> None:
    """When a dungeon_master is set, its narration should be used instead of plain text."""
    from unittest.mock import MagicMock

    mock_dm = MagicMock()
    mock_dm.narrate_action.return_value = "A fireball scorches the goblin!"

    combat = Combat(make_player(), make_enemy(), dungeon_master=mock_dm)

    with patch("builtins.input", side_effect=["1"]), \
         patch("dndgame.combat.roll", side_effect=[15, 6]):
        combat.start()

    mock_dm.narrate_action.assert_called()    