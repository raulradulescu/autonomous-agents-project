from __future__ import annotations

from ..core.constants import (
    COMPROMISED,
    HEALTHY,
    PATCHED,
    QUARANTINED,
    EXPLOIT,
    PHISH,
)
from ..core.utils import safe_choice
from .base import BaseAgent


class AttackerAgent(BaseAgent):
    role = "attacker"

    def __init__(self, unique_id, model, skill: float = 0.5):
        super().__init__(unique_id, model)
        self.skill = float(skill)

    def step(self):
        neighbors = list(self.model.G.neighbors(self.pos))
        if not neighbors:
            return
        target_node = safe_choice(neighbors, self.model.random)
        state = self.model.G.nodes[target_node]["state"]
        if state == QUARANTINED:
            return

        cell_agents = self.model.grid.get_cell_list_contents([target_node])
        has_user = any(getattr(a, "role", None) == "user" for a in cell_agents)
        action = PHISH if (has_user and self.model.random.random() < 0.5) else EXPLOIT
        success = False
        if action == EXPLOIT and state in (HEALTHY, PATCHED):
            base = self.skill
            if state == PATCHED:
                base *= 0.4
            success = self.model.random.random() < base
            if success:
                self.model.G.nodes[target_node]["state"] = COMPROMISED
        elif action == PHISH:
            users = [a for a in cell_agents if getattr(a, "role", None) == "user"]
            if users:
                user = safe_choice(users, self.model.random)
                consider = getattr(user, "consider_phish", None)
                if callable(consider):
                    success = bool(consider())
                    if success:
                        self.model.G.nodes[target_node]["state"] = COMPROMISED

        self.model.log_interaction(self.unique_id, int(target_node), action, success)
