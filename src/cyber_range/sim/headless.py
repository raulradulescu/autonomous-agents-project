from __future__ import annotations

from ..model.cyber_range import CyberRangeModel


def run_headless(
    steps: int = 300,
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
):
    model = CyberRangeModel(
        num_nodes=num_nodes,
        k=k,
        p=p,
        num_attackers=num_attackers,
        num_defenders=num_defenders,
        num_users=num_users,
        attacker_skill=attacker_skill,
        defender_diligence=defender_diligence,
        user_click_prob=user_click_prob,
        seed=seed,
    )
    for _ in range(steps):
        model.step()
    return model

