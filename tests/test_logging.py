from __future__ import annotations

import csv
from pathlib import Path
import tempfile

from cyber_range.model.cyber_range import CyberRangeModel


def test_log_interaction_and_dump_csv():
    m = CyberRangeModel(num_nodes=5, num_attackers=0, num_defenders=0, num_users=0, seed=3)
    m.log_interaction("A0", 1, "scan", True)
    assert len(m.interactions) == 1
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "out.csv"
        m.dump_interactions(str(out))
        assert out.exists()
        with out.open() as f:
            r = csv.reader(f)
            rows = list(r)
        assert rows[0] == ["step", "src_agent", "dst_node", "action", "success"]
        assert len(rows) == 2

