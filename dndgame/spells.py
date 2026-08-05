from __future__ import annotations

from dndgame.entity import Entity


class Spell:
    """Represent a single castable spell.

    Attributes:
        name: The spell's display name.
        level: The minimum spell level required to cast it.
        school: The magic school the spell belongs to (e.g. "Evocation").
        spell_power: The spell's power rating, used to scale its effect.
    """

    def __init__(self, name: str, level: int, school: str, spell_power: int) -> None:
        """Initialize a spell.

        Args:
            name: The spell's display name.
            level: The minimum spell level required to cast it.
            school: The magic school the spell belongs to.
            spell_power: The spell's power rating.
        """
        self.name = name
        self.level = level
        self.school = school
        self.spell_power = spell_power

    def cast(self, caster: Entity, target: Entity) -> int:
        """Cast this spell from a caster onto a target.

        Spells in this simplified system always hit and deal flat damage
        equal to the spell's spell_power directly to the target's HP.

        Args:
            caster: The character casting the spell.
            target: The character the spell is cast on.

        Returns:
            The amount of damage dealt.
        """
        target.hp -= self.spell_power
        return self.spell_power


class SpellBook:
    """Hold a collection of spells known by a character."""

    def __init__(self) -> None:
        """Initialize an empty spellbook."""
        self.spells: list[Spell] = []

    def add_spell(self, spell: Spell) -> None:
        """Add a spell to the spellbook.

        Args:
            spell: The spell to add.
        """
        self.spells.append(spell)

    def get_available_spells(self, spell_level: int) -> list[Spell]:
        """Get all spells castable at or below a given level.

        Args:
            spell_level: The maximum spell level to include.

        Returns:
            Spells whose level is less than or equal to spell_level.
        """
        available = []
        for spell in self.spells:
            if spell.level <= spell_level:
                available.append(spell)
        return available