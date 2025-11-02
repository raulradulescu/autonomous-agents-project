from __future__ import annotations

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, NetworkModule

from ..model.cyber_range import CyberRangeModel
from ..viz.network import network_portrayal
from ..viz.stats import StatsElement


def run_server():
    # Chart showing node states over time (LEFT SIDE)
    chart = ChartModule(
        [
            {"Label": "healthy", "Color": "#2ca02c"},
            {"Label": "compromised", "Color": "#d62728"},
            {"Label": "patched", "Color": "#1f77b4"},
            {"Label": "quarantined", "Color": "#9467bd"},
        ],
        data_collector_name="datacollector"
    )
    
    # Network visualization (RIGHT SIDE)
    net = NetworkModule(network_portrayal, 500, 500)
    
    # Stats text panel
    stats = StatsElement()
    
    server = ModularServer(
        CyberRangeModel,
        [chart, net, stats],  # Order: chart left, network right, stats below
        "Cyber-Range Simulation",
        {
            "num_nodes": 20,
            "k": 4,
            "p": 0.15,
            "num_attackers": 2,
            "num_defenders": 3,
            "num_users": 10,
            "attacker_skill": 0.55,
            "defender_diligence": 0.65,
            "user_click_prob": 0.25,
            "seed": 42,
        },
    )
    server.port = 8530
    server.launch()


if __name__ == "__main__":
    run_server()
