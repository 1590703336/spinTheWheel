"""Reusable helpers for exposing the quiz game over HTTP."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

from .game_data import GAME_DATA, SPECIAL_TILES, WINNING_SCORE

QUESTION_ID_SEPARATOR = "::"


@dataclass(frozen=True)
class Question:
    """Serializable question DTO for the API layer."""

    id: str
    group: str
    prompt: str
    answer: str


def list_groups() -> List[Dict[str, object]]:
    """Return all group names with the number of questions inside."""
    groups = []
    for group_name, questions in GAME_DATA.items():
        groups.append(
            {
                "id": group_name,
                "label": group_name,
                "questionCount": len(questions),
            }
        )
    return groups


def _encode_question_id(group: str, index: int) -> str:
    return f"{group}{QUESTION_ID_SEPARATOR}{index}"


def _decode_question_id(question_id: str) -> Tuple[str, int]:
    if QUESTION_ID_SEPARATOR not in question_id:
        raise ValueError("Invalid question id")
    group, index_str = question_id.split(QUESTION_ID_SEPARATOR, 1)
    index = int(index_str)
    return group, index


def _build_question(group: str, index: int) -> Question:
    data = GAME_DATA[group][index]
    return Question(
        id=_encode_question_id(group, index),
        group=group,
        prompt=data["q"],
        answer=data["a"],
    )


def get_question_by_id(question_id: str) -> Question:
    group, index = _decode_question_id(question_id)
    if group not in GAME_DATA or index >= len(GAME_DATA[group]):
        raise ValueError("Question does not exist")
    return _build_question(group, index)


def random_group(excluded: Optional[Iterable[str]] = None) -> str:
    excluded_set = set(excluded or [])
    choices = [group for group in GAME_DATA.keys() if group not in excluded_set]
    if not choices:
        raise ValueError("No groups available to pick from.")
    return random.choice(choices)


def random_question(
    group: str, excluded_ids: Optional[Iterable[str]] = None
) -> Question:
    if group not in GAME_DATA:
        raise ValueError("Unknown group.")
    excluded_set = set(excluded_ids or [])
    valid_indexes = [
        idx
        for idx in range(len(GAME_DATA[group]))
        if _encode_question_id(group, idx) not in excluded_set
    ]
    if not valid_indexes:
        raise ValueError("No more questions available in this group.")
    index = random.choice(valid_indexes)
    return _build_question(group, index)


def score_with_special_tiles(
    current_score: int, earned_points: int
) -> Dict[str, object]:
    """
    Add the earned points and apply a potential special tile effect.

    Returns a dict with the new score and metadata about special tile events so
    the caller can surface the same experience as the desktop app
    (`spinTheWheel.py` lines ~899-933).
    """
    base_score = current_score + earned_points
    special_event = None

    if base_score in SPECIAL_TILES:
        effect = SPECIAL_TILES[base_score]
        steps = random.randint(1, 5)

        if effect == "forward":
            base_score += steps
            special_event = {
                "type": "forward",
                "steps": steps,
                "message": f"🚀 LUCKY! Forward {steps} steps!",
            }
        else:
            base_score -= steps
            special_event = {
                "type": "backward",
                "steps": steps,
                "message": f"⚠️ OOPS! Backward {steps} steps!",
            }

        base_score = max(0, base_score)

    has_won = base_score >= WINNING_SCORE

    return {
        "score": base_score,
        "hasWinner": has_won,
        "specialEvent": special_event,
    }

