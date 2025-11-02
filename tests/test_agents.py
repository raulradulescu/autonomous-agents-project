from __future__ import annotations

from cyber_range.model.cyber_range import CyberRangeModel
from cyber_range.core.constants import COMPROMISED, QUARANTINED, PATCHED


def _first_agent_with_role(model: CyberRangeModel, role: str):
    for a in model.schedule.agents:
        if getattr(a, "role", None) == role:
            return a
    raise AssertionError(f"No agent with role={role}")


def test_defender_remediates_compromised_node():
    # Run multiple steps to increase chances of detection, or test the specific scenario
    m = CyberRangeModel(num_nodes=3, k=2, num_attackers=0, num_defenders=1, num_users=0, seed=4, defender_diligence=1.0)
    defender = _first_agent_with_role(m, "defender")
    # Move defender to a known node and mark ALL nodes compromised except defender's position
    target_node = list(m.G.nodes)[0]
    m.grid.move_agent(defender, target_node)
    # Mark all nodes as compromised - defender will eventually encounter one
    for node in m.G.nodes:
        m.G.nodes[node]["state"] = COMPROMISED
    
    # Run a few steps - with diligence=1.0, defender should remediate at least one node
    initial_compromised_count = sum(1 for _, v in m.G.nodes(data=True) if v["state"] == COMPROMISED)
    for _ in range(5):  # Multiple steps to ensure detection
        m.step()
    final_compromised_count = sum(1 for _, v in m.G.nodes(data=True) if v["state"] == COMPROMISED)
    
    # At least one node should have been remediated (count should decrease)
    assert final_compromised_count < initial_compromised_count


def test_attacker_respects_quarantine():
    # Minimal setting with one attacker and a quarantined neighbor
    m = CyberRangeModel(num_nodes=3, k=2, num_attackers=1, num_defenders=0, num_users=0, seed=5, attacker_skill=1.0)
    attacker = _first_agent_with_role(m, "attacker")
    # Place attacker on node 0 and quarantine a specific neighbor
    attacker_node = list(m.G.nodes)[0]
    neighbors = list(m.G.neighbors(attacker_node))
    assert neighbors, "Graph must provide a neighbor for the attacker"
    target_node = neighbors[0]
    m.grid.move_agent(attacker, attacker_node)
    m.G.nodes[target_node]["state"] = QUARANTINED
    m.step()
    # Quarantined node should remain quarantined after the step
    assert m.G.nodes[target_node]["state"] == QUARANTINED


def test_user_phish_probability_zero():
    # With click_prob=0.0, phishing should never succeed
    m = CyberRangeModel(num_nodes=4, num_attackers=0, num_defenders=0, num_users=1, seed=6, user_click_prob=0.0)
    user = _first_agent_with_role(m, "user")
    assert user.consider_phish() is False

