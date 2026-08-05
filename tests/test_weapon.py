from dndgame.weapon import Weapon


def test_weapon_stores_name_and_damage_die() -> None:
    """A Weapon should store its name and damage die correctly."""
    weapon = Weapon("Longsword", 8)

    assert weapon.name == "Longsword"
    assert weapon.damage_die == 8