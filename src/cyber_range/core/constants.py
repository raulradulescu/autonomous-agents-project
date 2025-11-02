from typing import Final

HEALTHY: Final[str] = "healthy"
COMPROMISED: Final[str] = "compromised"
PATCHED: Final[str] = "patched"
QUARANTINED: Final[str] = "quarantined"

# Action names used in interaction logs
PROBE: Final[str] = "probe"
EXPLOIT: Final[str] = "exploit"
PHISH: Final[str] = "phish"
SCAN: Final[str] = "scan"
PATCH: Final[str] = "patch"
QUARANTINE: Final[str] = "quarantine"


def node_state_color(state: str) -> str:
    if state == COMPROMISED:
        return "#d62728"  # red
    if state == PATCHED:
        return "#1f77b4"  # blue
    if state == QUARANTINED:
        return "#9467bd"  # purple
    return "#2ca02c"  # green for healthy
