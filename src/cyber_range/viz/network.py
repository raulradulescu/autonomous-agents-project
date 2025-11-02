from __future__ import annotations

from ..core.constants import node_state_color


def network_portrayal(G):
    """Portrayal function for Mesa NetworkModule - takes the graph as parameter."""
    
    def node_portrayal(node):
        state = G.nodes[node]["state"]
        return {
            "size": 6,
            "color": node_state_color(state),
            "tooltip": f"Node {node}: {state}",
        }

    def edge_portrayal(source, target):
        return {"color": "#e8e8e8", "width": 2}

    portrayal = {"nodes": [], "edges": []}
    
    # Add all nodes
    for node in G.nodes():
        portrayal["nodes"].append({
            "id": node,
            **node_portrayal(node)
        })
    
    # Add all edges  
    for source, target in G.edges():
        portrayal["edges"].append({
            "id": f"{source}-{target}",
            "source": source,
            "target": target,
            **edge_portrayal(source, target)
        })
    
    return portrayal

