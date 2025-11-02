# autonomous-agents-project

Agent-based cyber-range simulation on a network graph built with Mesa + NetworkX. Three agent types (attacker, defender, user) interact over a small-world enterprise-like topology. Node states evolve (healthy/compromised/patched/quarantined) and are shown live in an interactive browser visualization with real-time charts and network graphs.

## What's Included
- Mesa model (`CyberRangeModel`) with deterministic seeding
- Agents: Attacker, Defender, User with distinct behaviors
- Interactive browser visualization with:
  - Side-by-side layout: line chart (left) and network topology (right)
  - Stable network graph with fixed node positions
  - Real-time color-coded nodes: green (healthy), red (compromised), blue (patched), purple (quarantined)
  - Live statistics panel
- Headless runner that exports interactions to CSV
- Comprehensive unit tests supporting TDD

## Features

### Agent Behaviors
- **Attackers**: Probe neighbors, exploit infrastructure, and send phishing attacks. Success rates depend on skill level and target state (reduced against patched nodes).
- **Defenders**: Scan for threats, patch vulnerable systems, and quarantine compromised nodes. Detection based on diligence parameter.
- **Users**: Move around the network and may click on phishing attempts (probability reduced when defenders are present).

### Network Dynamics
- **Node States**: Healthy → Compromised → Patched/Quarantined
- **Small-World Topology**: Realistic enterprise-like network structure using Watts-Strogatz model
- **Deterministic Seeding**: Reproducible simulations for analysis and debugging

## Project Structure
```
.
├─ Project-Architecture.md
├─ README.md
├─ requirements.txt
├─ scripts/
│  └─ run_headless.py               # CLI to run simulation and export CSV
├─ src/
│  └─ cyber_range/
│     ├─ __init__.py
│     ├─ agents/
│     │  ├─ __init__.py
│     │  ├─ attacker.py
│     │  ├─ defender.py
│     │  ├─ base.py
│     │  └─ user.py
│     ├─ core/
│     │  ├─ constants.py            # states, action names, color mapping
│     │  ├─ types.py                # Interaction tuple, NodeId alias
│     │  └─ utils.py                # helpers
│     ├─ env/
│     │  ├─ graph_builder.py        # NetworkX graph factory (healthy init)
│     │  └─ grid.py                 # Mesa NetworkGrid wrapper
│     ├─ model/
│     │  ├─ cyber_range.py          # Mesa Model wiring, step, logging
│     │  ├─ datacollection.py       # DataCollector setup
│     │  └─ interactions.py         # CSV export helper
│     ├─ sim/
│     │  ├─ headless.py             # Programmatic headless runs
│     │  └─ run_server.py           # Mesa server (alternative)
│     └─ viz/
│        ├─ network.py              # network portrayal
│        ├─ stats.py                # stats panel
│        ├─ simple_server.py        # custom visualization server
│        └─ templates/
│           └─ index.html           # interactive web interface
└─ tests/
   ├─ test_agents.py
   ├─ test_logging.py
   └─ test_model.py
```

## Quickstart

### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Set up Python environment (recommended)
The project uses a virtual environment for clean dependency management:
```powershell
# Windows - the environment is automatically configured
# Just run the visualization commands below
```

### 3) Launch the interactive visualization
**Windows PowerShell:**
```powershell
$env:PYTHONPATH = 'src'
.venv/Scripts/python.exe -m cyber_range.viz.simple_server
```

**macOS/Linux:**
```bash
PYTHONPATH=src python -m cyber_range.viz.simple_server
```

The server starts on `http://127.0.0.1:8555` by default. Open this in your browser to see:
- **Left Panel**: Line chart showing node state evolution over time
- **Right Panel**: Interactive network topology with color-coded nodes and visible edges
- **Bottom Panel**: Live statistics (step count, state counts)

**Visualization Features:**
- **Green nodes** 🟢 = Healthy systems
- **Red nodes** 🔴 = Compromised systems  
- **Blue nodes** 🔵 = Patched systems
- **Purple nodes** 🟣 = Quarantined systems
- **Gray lines** = Network connections

**Controls:**
- **Start/Pause**: Run or pause the simulation
- **Step**: Advance one time step manually
- **Reset**: Restart with a new simulation (repositions network)
- **FPS Slider**: Control simulation speed (1-20 frames per second)
- **Drag Nodes**: Click and drag nodes to rearrange them (positions are preserved)

### 4) Run headless simulation and export data
For batch experiments or data collection without the GUI:

**Windows PowerShell:**
```powershell
$env:PYTHONPATH = 'src'
.venv/Scripts/python.exe scripts/run_headless.py --steps 300 --out interactions.csv --seed 42
```

**macOS/Linux:**
```bash
PYTHONPATH=src python scripts/run_headless.py --steps 300 --out interactions.csv --seed 42
```

**Available arguments:**
- `--steps`: Number of simulation steps (default: 300)
- `--out`: Output CSV file path (default: interactions.csv)
- `--seed`: Random seed for reproducibility (default: 42)
- `--num-nodes`: Number of network nodes (default: 20)
- `--num-attackers`: Number of attacker agents (default: 2)
- `--num-defenders`: Number of defender agents (default: 3)
- `--num-users`: Number of user agents (default: 10)

## Testing
Run the unit tests (deterministic with seeds):

**Windows PowerShell:**
```powershell
$env:PYTHONPATH = 'src'
.venv/Scripts/python.exe -m pytest tests/ -v
```

**macOS/Linux:**
```bash
PYTHONPATH=src pytest tests/ -v
```

All tests should pass with green checkmarks ✓

## Data and Logging
- **Interaction records**: `(step, src_agent, dst_node, action, success)` where `success` is 0/1
- **Export CSV**: via headless script or `CyberRangeModel.dump_interactions(path)`
- **Sample data**: Each row represents an agent action (scan, exploit, patch, phish, quarantine)

Example CSV output:
```csv
step,src_agent,dst_node,action,success
1,D0,6,patch,1
1,A1,11,exploit,1
2,A0,5,exploit,0
2,D1,7,scan,0
```

## Configuration

### Model Parameters
All simulations can be customized with these parameters:
- `num_nodes` (int): Number of network nodes (default: 20)
- `k` (int): Number of neighbors in small-world graph (default: 4)
- `p` (float): Rewiring probability for small-world graph (default: 0.15)
- `num_attackers` (int): Number of attacker agents (default: 2)
- `num_defenders` (int): Number of defender agents (default: 3)
- `num_users` (int): Number of user agents (default: 10)
- `attacker_skill` (float): Probability of successful exploit (default: 0.55)
- `defender_diligence` (float): Probability of detecting compromise (default: 0.65)
- `user_click_prob` (float): Probability of clicking phishing (default: 0.25)
- `seed` (int): Random seed for reproducibility (default: 42)

## How It Works

### Simulation Loop
1. **Initialization**: Network created with all nodes healthy
2. **Agent Placement**: Agents randomly placed on network nodes
3. **Each Step**:
   - Attackers attempt to exploit or phish
   - Defenders scan and remediate threats
   - Users move around (may click phishing)
   - States update based on successful actions
   - Data collector records current state counts
4. **Visualization Updates**: Browser displays new states in real-time

### Attack-Defense Dynamics
- Attackers have **higher success** against healthy nodes
- Patched nodes are **harder to exploit** (40% of normal success rate)
- Defenders **detect compromised** nodes based on diligence
- Defenders **patch preventively** (20% chance on healthy nodes)
- Users are **less likely** to click phishing when defenders are present (50% reduction)

## Next Steps & Extensions

### Planned Features
- **YAML Configuration**: External config files for easier parameter tuning
- **Shell Scripts**: Convenience scripts for common workflows
- **IDS Agent**: Intrusion detection system that alerts on suspicious patterns
- **User Training**: Gradual reduction in click_prob over time
- **Cost/Utility Model**: Track downtime penalties and remediation costs
- **Heterogeneous Nodes**: Different roles (server/workstation/router) with varying vulnerability
- **Playback Mode**: Save and replay simulations frame-by-frame

### Research & Analysis Ideas
- Compare different defender strategies (reactive vs. proactive patching)
- Measure impact of user training on overall security posture
- Optimize defender-to-attacker ratios for different network sizes
- Study propagation patterns in different network topologies
- Evaluate cost-effectiveness of different defense investments

### Developer Improvements
- GitHub Actions CI/CD pipeline
- Expanded test coverage for edge cases
- Pin exact dependency versions
- Docker containerization
- API for programmatic control

## Troubleshooting

### Port Already in Use
If you see `OSError: [WinError 10048]`, the port is already in use. Either:
- Close the previous server instance
- Or edit `src/cyber_range/viz/simple_server.py` to use a different port

### Module Not Found
If you see `ModuleNotFoundError: No module named 'cyber_range'`:
- Make sure you set `PYTHONPATH=src` before running commands
- Or run from the project root directory

### Missing Dependencies
If you see import errors:
```bash
pip install -r requirements.txt
```

## Contributing
This project follows TDD principles. When adding features:
1. Write tests first (`tests/`)
2. Implement the feature
3. Run tests to verify: `pytest tests/ -v`
4. Update documentation

## License
See `LICENSE` file for details.

## Architecture
For detailed implementation guidance and build plan, see `Project-Architecture.md`.
