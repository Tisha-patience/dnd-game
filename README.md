# D&D Adventure System

A text-based D&D-style adventure game system that needs improvements and new features. This project serves as a learning exercise for implementing professional Python development practices.

> **Note about D&D**: Dungeons & Dragons (D&D) is a fantasy role-playing game where players create characters with different abilities (like strength and dexterity) and engage in combat using dice rolls to determine outcomes. Don't worry if you're not familiar with D&D - this project uses a very simplified version of its mechanics, and all the game rules you need to know are implemented in the code!

## Current Features
- Basic character creation with races (Human, Elf, Dwarf)
- Stat rolling system with racial bonuses
- Simple combat mechanics
- Dice rolling utilities

## Setup

1. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Development Commands

### Running the Game
```bash
python main.py
```

### Running Tests
```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=dndgame

# Run specific test file
pytest tests/test_dice.py
```

### Type Checking
```bash
mypy dndgame --strict
```

### Code Formatting
```bash
black .
```

## Optional: AI-Narrated Combat

The game supports AI-narrated combat via OpenAI's API. This is fully
optional — the game works normally with plain text combat messages
without it.

To enable it:
1. Create a `.env` file in the project root (never commit this file):
2. In `main.py`, pass a `DungeonMaster()` instance when creating combat:
```python
   from dndgame.dungeon_master import DungeonMaster
   combat = Combat(player, enemy, dungeon_master=DungeonMaster())
```

If the API call fails for any reason (missing key, network issue,
rate limit), combat automatically falls back to the standard plain
text messages — the game will never crash because of this feature.



## Additional Resources

- [Python Type Hints Documentation](https://docs.python.org/3/library/typing.html)
- [pytest Documentation](https://docs.pytest.org/)
- [mypy Documentation](https://mypy.readthedocs.io/)