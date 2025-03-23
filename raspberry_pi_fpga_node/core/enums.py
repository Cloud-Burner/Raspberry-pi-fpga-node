"""This module contains the local enums."""

from enum import StrEnum


class LangExecutionType(StrEnum):
    """Enumeration of lang types"""

    HARD = "hard"
    OPTIMIZED = "optimized"
    LITE = "lite"
