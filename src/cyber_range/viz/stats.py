from __future__ import annotations

from mesa.visualization.modules import TextElement

from ..core.constants import COMPROMISED, HEALTHY, PATCHED, QUARANTINED


class StatsElement(TextElement):
    def render(self, model):
        healthy = sum(1 for _, v in model.G.nodes(data=True) if v["state"] == HEALTHY)
        compromised = sum(1 for _, v in model.G.nodes(data=True) if v["state"] == COMPROMISED)
        patched = sum(1 for _, v in model.G.nodes(data=True) if v["state"] == PATCHED)
        quarantined = sum(1 for _, v in model.G.nodes(data=True) if v["state"] == QUARANTINED)
        return (
            f"Step: {model.step_count} | "
            f"Healthy: {healthy} | Compromised: {compromised} | "
            f"Patched: {patched} | Quarantined: {quarantined}"
        )

