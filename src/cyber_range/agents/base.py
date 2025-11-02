from __future__ import annotations

from typing import Optional

from mesa import Agent


class BaseAgent(Agent):
    """Base class setting a textual role for cross-agent checks without import cycles."""

    role: str = "base"

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # Position (node id) is set by the grid when placed
        self.pos: Optional[int] = None

