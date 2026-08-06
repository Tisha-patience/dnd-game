from __future__ import annotations

from typing import Any

from decouple import config
from openai import OpenAI


class DungeonMaster:
    """Narrate combat actions using an AI model.

    Attributes:
        client: The OpenAI client used to make chat requests.
    """

    def __init__(self) -> None:
        """Initialize the DungeonMaster with an OpenAI API client."""
        api_key = config("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

    def narrate_action(
        self,
        actor_name: str,
        action: str,
        target_name: str,
        damage: int,
    ) -> str:
        """Generate a short fantasy narration for an action.

        Args:
            actor_name: The name of the acting character.
            action: The action being performed.
            target_name: The name of the target character.
            damage: The amount of damage dealt.

        Returns:
            A single short sentence narrating the action.
        """
        prompt = (
            f"Narrate in one short fantasy sentence: {actor_name} {action} "
            f"against {target_name}"
        )
        if damage:
            prompt += f" for {damage} damage."
        else:
            prompt += " but misses."

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a fantasy combat narrator."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=40,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            if damage:
                return f"{actor_name} attacks {target_name} for {damage} damage!"
            return f"{actor_name} attacks {target_name} but misses!"
