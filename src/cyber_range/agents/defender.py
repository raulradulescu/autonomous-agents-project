from __future__ import annotations

from ..core.constants import (
    COMPROMISED,
    HEALTHY,
    PATCHED,
    QUARANTINED,
    PATCH,
    QUARANTINE,
    SCAN,
)
from ..core.utils import safe_choice
from .base import BaseAgent


class DefenderAgent(BaseAgent):
    role = "defender"

    def __init__(self, unique_id, model, diligence: float = 0.6):
        super().__init__(unique_id, model)
        self.diligence = float(diligence)

    def step(self):
        candidates = [self.pos] + list(self.model.G.neighbors(self.pos))
        target_node = safe_choice(candidates, self.model.random)
        state = self.model.G.nodes[target_node]["state"]

        found = (state == COMPROMISED) and (self.model.random.random() < self.diligence)
        if found:
            if self.model.random.random() < 0.7:
                self.model.G.nodes[target_node]["state"] = PATCHED
                self.model.log_interaction(self.unique_id, int(target_node), PATCH, True)
            else:
                self.model.G.nodes[target_node]["state"] = QUARANTINED
                self.model.log_interaction(self.unique_id, int(target_node), QUARANTINE, True)
        else:
            if state == HEALTHY and (self.model.random.random() < 0.2):
                self.model.G.nodes[target_node]["state"] = PATCHED
                self.model.log_interaction(self.unique_id, int(target_node), PATCH, True)
            else:
                self.model.log_interaction(self.unique_id, int(target_node), SCAN, False)

