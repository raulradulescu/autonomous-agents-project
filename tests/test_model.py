from __future__ import annotations

from cyber_range.model.cyber_range import CyberRangeModel
from cyber_range.core.constants import HEALTHY, COMPROMISED, PATCHED, QUARANTINED


def test_model_initialization_states_all_healthy():
    m = CyberRangeModel(num_nodes=10, num_attackers=0, num_defenders=0, num_users=0, seed=1)
    assert len(m.interactions) == 0
    states = [v["state"] for _, v in m.G.nodes(data=True)]
    assert all(s == HEALTHY for s in states)


def test_counts_sum_to_num_nodes_after_step():
    m = CyberRangeModel(num_nodes=15, num_attackers=1, num_defenders=1, num_users=1, seed=2)
    m.step()
    healthy = sum(1 for _, v in m.G.nodes(data=True) if v["state"] == HEALTHY)
    compromised = sum(1 for _, v in m.G.nodes(data=True) if v["state"] == COMPROMISED)
    patched = sum(1 for _, v in m.G.nodes(data=True) if v["state"] == PATCHED)
    quarantined = sum(1 for _, v in m.G.nodes(data=True) if v["state"] == QUARANTINED)
    assert healthy + compromised + patched + quarantined == m.G.number_of_nodes()

