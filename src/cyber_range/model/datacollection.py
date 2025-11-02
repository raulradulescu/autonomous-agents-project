from __future__ import annotations

from mesa.datacollection import DataCollector

from ..core.constants import COMPROMISED, HEALTHY, PATCHED, QUARANTINED


def make_datacollector():
    return DataCollector(
        model_reporters={
            "healthy": lambda m: sum(1 for _, v in m.G.nodes(data=True) if v["state"] == HEALTHY),
            "compromised": lambda m: sum(1 for _, v in m.G.nodes(data=True) if v["state"] == COMPROMISED),
            "patched": lambda m: sum(1 for _, v in m.G.nodes(data=True) if v["state"] == PATCHED),
            "quarantined": lambda m: sum(1 for _, v in m.G.nodes(data=True) if v["state"] == QUARANTINED),
        }
    )

