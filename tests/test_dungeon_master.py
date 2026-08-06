from unittest.mock import MagicMock, patch

from dndgame.dungeon_master import DungeonMaster


def test_narrate_action_falls_back_on_api_failure() -> None:
    """If the OpenAI call fails, narrate_action should use the fallback text."""
    with patch("dndgame.dungeon_master.config", return_value="fake-key"):
        dm = DungeonMaster()

    dm.client = MagicMock()
    dm.client.chat.completions.create.side_effect = Exception("API is down")

    result = dm.narrate_action("Hero", "attacks", "Goblin", 5)

    assert result == "Hero attacks Goblin for 5 damage!"


def test_narrate_action_falls_back_with_miss_message_on_api_failure() -> None:
    """If the OpenAI call fails and there's no damage, the fallback should say 'misses'."""
    with patch("dndgame.dungeon_master.config", return_value="fake-key"):
        dm = DungeonMaster()

    dm.client = MagicMock()
    dm.client.chat.completions.create.side_effect = Exception("API is down")

    result = dm.narrate_action("Hero", "attacks", "Goblin", 0)

    assert result == "Hero attacks Goblin but misses!"


def test_narrate_action_returns_model_content_on_success() -> None:
    """On a successful API call, narrate_action should return the model's text."""
    with patch("dndgame.dungeon_master.config", return_value="fake-key"):
        dm = DungeonMaster()

    fake_response = MagicMock()
    fake_response.choices[0].message.content = "The blade finds its mark!"
    dm.client = MagicMock()
    dm.client.chat.completions.create.return_value = fake_response

    result = dm.narrate_action("Hero", "attacks", "Goblin", 5)

    assert result == "The blade finds its mark!"