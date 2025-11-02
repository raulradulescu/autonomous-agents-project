from __future__ import annotations

from ..core.constants import HEALTHY
from .base import BaseAgent


class UserAgent(BaseAgent):
    role = "user"

    def __init__(self, unique_id, model, click_prob: float = 0.2):
        super().__init__(unique_id, model)
        self.click_prob = float(click_prob)

    def consider_phish(self) -> bool:
        cell_agents = self.model.grid.get_cell_list_contents([self.pos])
        has_defender = any(getattr(a, "role", None) == "defender" for a in cell_agents)
        p = self.click_prob * (0.5 if has_defender else 1.0)
        return self.model.random.random() < p

    def step(self):
        neighbors = list(self.model.G.neighbors(self.pos))
        if neighbors and self.model.random.random() < 0.1:
            self.model.grid.move_agent(self, self.model.random.choice(neighbors))

