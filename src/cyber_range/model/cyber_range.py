from __future__ import annotations

from typing import List, Tuple

from mesa import Model
from mesa.space import NetworkGrid
from mesa.time import RandomActivation

from ..agents import AttackerAgent, DefenderAgent, UserAgent
from ..core.constants import (
    HEALTHY,
)
from ..model.datacollection import make_datacollector
from ..model.interactions import dump_interactions as dump_interactions_to_csv
from ..env.graph_builder import build_graph
from ..env.grid import make_grid


class CyberRangeModel(Model):
    """Mesa model for the cyber-range simulation.

    Parameters allow deterministic tests and quick experiments.
    """

    def __init__(
        self,
        *,
        num_nodes: int = 20,
        k: int = 4,
        p: float = 0.15,
        num_attackers: int = 2,
        num_defenders: int = 3,
        num_users: int = 10,
        attacker_skill: float = 0.55,
        defender_diligence: float = 0.65,
        user_click_prob: float = 0.25,
        seed: int | None = None,
    ) -> None:
        super().__init__(seed=seed)

        self.G = build_graph(num_nodes=num_nodes, k=k, p=p, seed=seed)
        self.grid: NetworkGrid = make_grid(self.G)
        self.schedule = RandomActivation(self)
        self.step_count = 0
        self.interactions: List[Tuple[int, str, int, str, int]] = []

        for i in range(num_attackers):
            a = AttackerAgent(f"A{i}", self, skill=attacker_skill)
            self.schedule.add(a)
            self.grid.place_agent(a, self.random.choice(list(self.G.nodes)))
        for i in range(num_defenders):
            d = DefenderAgent(f"D{i}", self, diligence=defender_diligence)
            self.schedule.add(d)
            self.grid.place_agent(d, self.random.choice(list(self.G.nodes)))
        for i in range(num_users):
            u = UserAgent(f"U{i}", self, click_prob=user_click_prob)
            self.schedule.add(u)
            self.grid.place_agent(u, self.random.choice(list(self.G.nodes)))

        self.datacollector = make_datacollector()

    # Logging API
    def log_interaction(self, src_agent_id: str, dst_node: int, action: str, success: bool) -> None:
        self.interactions.append((self.step_count, src_agent_id, int(dst_node), action, int(bool(success))))

    def step(self) -> None:
        self.step_count += 1
        self.schedule.step()
        self.datacollector.collect(self)

    def dump_interactions(self, path: str = "interactions.csv") -> None:
        dump_interactions_to_csv(self.interactions, path)
