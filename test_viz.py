import sys
sys.path.insert(0, 'src')

from cyber_range.model.cyber_range import CyberRangeModel
from cyber_range.viz.network import network_portrayal
import json

# Create a small model
m = CyberRangeModel(num_nodes=5, num_attackers=1, num_defenders=1, num_users=1, seed=42)

# Test the portrayal
portrayal = network_portrayal(m.G)

print("=== Network Portrayal ===")
print(json.dumps(portrayal, indent=2))

# Step the model and check again
m.step()
print("\n=== After Step ===")
portrayal2 = network_portrayal(m.G)
print(json.dumps(portrayal2, indent=2))

# Check if nodes have expected structure
print("\n=== Checking node structure ===")
if portrayal["nodes"]:
    print(f"First node: {portrayal['nodes'][0]}")
    print(f"Has 'id': {'id' in portrayal['nodes'][0]}")
    print(f"Has 'color': {'color' in portrayal['nodes'][0]}")
    print(f"Has 'size': {'size' in portrayal['nodes'][0]}")
