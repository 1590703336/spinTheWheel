"""Backend package exposing shared game data and logic for web deployment."""

from .game_data import GAME_DATA, SPECIAL_TILES, WINNING_SCORE

__all__ = ["GAME_DATA", "SPECIAL_TILES", "WINNING_SCORE"]

