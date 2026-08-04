from main import prompt_menu_choice, prompt_non_empty_input


def test_prompt_non_empty_input_retries_until_it_receives_a_value(monkeypatch) -> None:
    """Blank input should be rejected until a real value is entered."""
    responses = iter(["", "   ", "Gimli"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(responses))

    assert prompt_non_empty_input("Enter your character's name: ") == "Gimli"


def test_prompt_menu_choice_retries_until_choice_is_within_range(monkeypatch) -> None:
    """Invalid menu selections should be rejected until a valid choice is entered."""
    responses = iter(["0", "9", "2"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(responses))

    assert prompt_menu_choice("Enter choice (1-3): ", 3) == 2
