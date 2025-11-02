# Project Architecture — Cyber-Range on a Graph (Mesa)

This document is a build plan tailored for a software-developer LLM agent to implement a small, visual agent‑based cyber‑range. It decomposes the work into concrete, verifiable steps with clear structure, acceptance criteria, and commands to run.

## Overview
- Goal: Simulate attacker–defender dynamics over a small enterprise network graph; nodes flip between healthy/compromised/patched/quarantined while interactions are logged and visualized in a browser.
- Agent types:
  - AttackerAgent — probes neighbors, exploits infra, or phishes users.
  - DefenderAgent — scans, patches, and quarantines compromised nodes.
  - UserAgent — benign movement; can click phishing with configurable probability.
- Tech: Python, Mesa (agents/scheduling/visualization), NetworkX (graph), optional CSV output for analysis.

## High-Level Architecture
- Runtime: Mesa `Model` + `RandomActivation` schedule; Mesa `NetworkGrid` wrapping a NetworkX graph.
- Data: Node attributes carry state; interactions list captures events for analysis.
- UI: Mesa `ModularServer` with a custom `NetworkModule` portrayal and a text stats panel.
- Config: Centralized defaults with optional YAML overrides.
- Tests: Deterministic with seed; unit tests for state transitions and logging.

## Repository Structure
Use a src/ layout for import clarity and packaging ergonomics.

```
.
├─ Project-Architecture.md
├─ README.md
├─ requirements.txt              # mesa, networkx, (pytest optional)
├─ pyproject.toml (optional)     # for editable installs; out-of-scope to commit now
├─ configs/
│  └─ experiment.yaml            # knobs: counts, graph params, seed, rates
├─ scripts/
│  ├─ run_server.ps1             # Windows helper
│  ├─ run_server.sh              # POSIX helper
│  ├─ run_headless.py            # CLI entry to run N steps and export CSV
│  └─ export_interactions.py     # Convert CSV -> charts (optional)
├─ src/
│  └─ cyber_range/
│     ├─ __init__.py
│     ├─ core/
│     │  ├─ constants.py         # HEALTHY/COMPROMISED/PATCHED/QUARANTINED, actions
│     │  ├─ types.py             # Typed aliases: NodeId, Interaction, etc.
│     │  └─ utils.py             # Coloring, RNG helpers, timestamping
│     ├─ config/
│     │  ├─ __init__.py
│     │  ├─ schema.py            # pydantic/dataclass config model (optional)
│     │  └─ defaults.yaml
│     ├─ env/
│     │  ├─ graph_builder.py     # NetworkX graph generation/import
│     │  └─ grid.py              # Mesa NetworkGrid helpers
│     ├─ agents/
│     │  ├─ __init__.py
│     │  ├─ base.py
│     │  ├─ attacker.py
│     │  ├─ defender.py
│     │  └─ user.py
│     ├─ model/
│     │  ├─ __init__.py
│     │  ├─ cyber_range.py       # The Mesa Model (scheduling, logging)
│     │  ├─ datacollection.py    # Mesa DataCollector setup
│     │  └─ interactions.py      # Logging, CSV export helpers
│     ├─ sim/
│     │  ├─ run_server.py        # Mesa ModularServer boot
│     │  └─ headless.py          # Pure-sim runner for experiments
│     └─ viz/
│        ├─ network.py           # portrayal for nodes/edges
│        └─ stats.py             # custom TextElement panel
└─ tests/
   ├─ test_agents.py
   ├─ test_model.py
   └─ test_logging.py
```

Notes:
- Choose either `requirements.txt` or `pyproject.toml` for dependency management. The simplest path is `requirements.txt` with `pip install -r requirements.txt` and `PYTHONPATH=src` when running modules.
- The single-file prototype (`cyber_agents.py`) maps directly into modular files above.

## Domain Model
- Node states: `HEALTHY`, `COMPROMISED`, `PATCHED`, `QUARANTINED`.
- Actions: `probe`, `exploit`, `phish`, `scan`, `patch`, `quarantine`.
- Interaction record: `(step: int, src_agent: str, dst_node: int, action: str, success: int)`.
- Config knobs: numbers of agents, seed, graph generator and params, agent rates (skill, diligence, click_prob), server port, run length.

## Core Responsibilities
- AttackerAgent
  - Select neighbor target; skip quarantined nodes.
  - Action selection: `exploit` infra or `phish` if users present.
  - Success depends on base skill and node state (reduced vs `PATCHED`).
  - On success, set node to `COMPROMISED`; log interaction.
- DefenderAgent
  - Scan current/neighbor node; with diligence detect compromise.
  - On finding: `patch` or `quarantine` (weighted choice); log.
  - Otherwise: opportunistic `patch` healthy nodes sometimes; log `scan`.
- UserAgent
  - Benign movement with small probability.
  - `consider_phish()`: reduced click probability if a defender is present in the cell.
- Model (CyberRangeModel)
  - Build/own graph and grid; create agents; schedule steps; collect metrics.
  - Maintain `interactions` list and an optional CSV export.

## Visualization
- `viz/network.py`: Node portrayal with color per state and simple edge rails.
- `viz/stats.py`: Text panel showing step and counts per state.
- `sim/run_server.py`: `ModularServer` that wires `NetworkModule` + `StatsElement`.

## Configuration
- Defaults live in `config/defaults.yaml`.
- Optional runtime overrides via a YAML path or env vars.
- Keep the first iteration simple: direct kwargs to `CyberRangeModel` and server.

## Logging, Metrics, and Analysis
- `model/interactions.py` offers `log_interaction()` and `dump_interactions(path)`.
- `model/datacollection.py` sets `DataCollector` fields: healthy, compromised, patched, quarantined.
- `scripts/run_headless.py` runs N steps headless, writes interactions CSV, and can print summary stats.

## Testing Strategy
- Determinism: every test uses fixed `seed`.
- Unit tests
  - Agents: exploitation success decreases on `PATCHED`; phishing respects `click_prob` and defender presence; defenders quarantine/patch on detection.
  - Model: logging structure and counts; DataCollector returns non-negative counts that sum to number of nodes.
  - Serialization: CSV header and row lengths as expected.

## LLM Developer Agent — Step Plan
Each step includes its acceptance criteria and quick commands. Prefer small, verifiable commits.

1) Bootstrap project
- Tasks: Create `src/` package, minimal `requirements.txt` with `mesa`, `networkx`, `pytest`.
- Accept: `python -c "import mesa, networkx"` succeeds; `pytest -q` runs 0 tests.
- Commands:
  - `pip install -r requirements.txt`

2) Core constants and types
- Tasks: Implement `core/constants.py` (states, actions) and `core/types.py` (TypedDict/NamedTuple for `Interaction`).
- Accept: imports succeed; constants used by later modules.

3) Graph + grid utilities
- Tasks: `env/graph_builder.py` with a function returning a connected small-world graph; `env/grid.py` to wrap in `NetworkGrid`.
- Accept: Graph is connected; nodes initialize with `state=HEALTHY`.

4) Base and concrete agents
- Tasks: `agents/base.py` (common utilities); implement `attacker.py`, `defender.py`, `user.py` per responsibilities.
- Accept: Agents import and instantiate with required parameters; no runtime errors on single step.

5) Model and data collection
- Tasks: `model/cyber_range.py` with schedule, placement, and `step()`; `model/datacollection.py` for counts; `model/interactions.py` for logging and CSV export.
- Accept: After several steps, counts are integers and interactions are appended.

6) Visualization wiring
- Tasks: `viz/network.py` portrayal function; `viz/stats.py` text element; `sim/run_server.py` to start `ModularServer`.
- Accept: Starting the server opens/serves visualization; nodes colored by state; stats update.

7) Headless runner and export
- Tasks: `sim/headless.py` (library) and `scripts/run_headless.py` (CLI) to run N steps and write CSV.
- Accept: CSV file exists, header correct, rows match `interactions` length.

8) Tests
- Tasks: Implement `tests/test_agents.py`, `tests/test_model.py`, `tests/test_logging.py`.
- Accept: `pytest -q` passes locally.

9) Docs and usage polish
- Tasks: Update `README.md` with run instructions; list key configs and extension ideas.
- Accept: New contributor can run server and headless flow following README only.

## Implementation Details and Snippets
- Node color mapping: gray/healthy, red/compromised, blue/patched, purple/quarantined.
- Interaction logging: call `log_interaction(agent_id, dst_node, action, success: bool)` from agents; store `int(success)` in records for CSV compactness.
- Defender detection: `found = (state == COMPROMISED) and (rand < diligence)`; on found, 70% patch, else quarantine.
- Attacker exploit vs patched: success base reduced by ~60% on `PATCHED`.
- User phishing: `p = click_prob * (0.5 if defender_present else 1.0)`.

## Run Instructions (once implemented)
- Install deps: `pip install -r requirements.txt`
- Launch UI: `PYTHONPATH=src python -m cyber_range.sim.run_server` (Windows PowerShell: `$env:PYTHONPATH='src'; python -m cyber_range.sim.run_server`)
- Headless: `PYTHONPATH=src python scripts/run_headless.py --steps 300 --out interactions.csv`

## Coding Standards for the LLM Agent
- Style: PEP8 + type hints for public functions.
- Tests: deterministic seeds; one behavior per test; avoid sleeps.
- Logging: keep interactions flat, immutable records; avoid embedding full agent objects.
- Errors: fail fast on invalid config; raise `ValueError` with actionable messages.
- Docstrings: module and public function docstrings explaining purpose and parameters.

## Acceptance Checklist (Definition of Done)
- Visual server starts and updates each tick.
- Node states evolve via agent actions; counts visible.
- Interactions collected and exported to CSV; schema stable.
- Tests pass on a clean environment.
- README documents both UI and headless workflows.

## Backlog and Extensions
- User training campaigns: decrease `click_prob` over time.
- IDS agent that alerts on suspicious action surges in a window.
- Costs/utility model: downtime penalties; attacker vs defender utility.
- Heterogeneous topology: roles (server/workstation/router) with different risks.
- Playback: store portrayal per step for time-sliced animation.

## Risks and Mitigations
- Nondeterminism: always allow a `seed` parameter; set in tests.
- Performance on large graphs: keep visualization small; headless for bigger runs.
- Dependency drift: pin major versions in `requirements.txt`.

---

This plan is intentionally incremental. Implement steps in order, verifying each acceptance criterion before proceeding. Keep PRs small and focused (one step per PR) to maintain velocity and reviewability.

