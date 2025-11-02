from __future__ import annotations

import csv
from typing import Iterable, Tuple


def dump_interactions(records: Iterable[Tuple[int, str, int, str, int]], path: str = "interactions.csv") -> None:
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["step", "src_agent", "dst_node", "action", "success"])
        for rec in records:
            w.writerow(list(rec))

