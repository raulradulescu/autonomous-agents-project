#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path

from cyber_range.sim.headless import run_headless


def main():
    p = argparse.ArgumentParser(description="Run headless cyber-range and export interactions CSV")
    p.add_argument("--steps", type=int, default=300)
    p.add_argument("--out", type=Path, default=Path("interactions.csv"))
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--num-nodes", type=int, default=20)
    p.add_argument("--k", type=int, default=4)
    p.add_argument("--p", type=float, default=0.15)
    p.add_argument("--num-attackers", type=int, default=2)
    p.add_argument("--num-defenders", type=int, default=3)
    p.add_argument("--num-users", type=int, default=10)
    args = p.parse_args()

    model = run_headless(
        steps=args.steps,
        num_nodes=args.num_nodes,
        k=args.k,
        p=args.p,
        num_attackers=args.num_attackers,
        num_defenders=args.num_defenders,
        num_users=args.num_users,
        seed=args.seed,
    )
    model.dump_interactions(str(args.out))
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
