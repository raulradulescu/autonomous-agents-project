"""Custom ModularServer with side-by-side layout."""
from __future__ import annotations

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, NetworkModule
from ..model.cyber_range import CyberRangeModel
from ..viz.network import network_portrayal
from ..viz.stats import StatsElement


class CustomModularServer(ModularServer):
    """Custom server with modified HTML template for side-by-side layout."""
    
    def render_model(self):
        """Override to inject custom CSS."""
        return super().render_model()
    
    def get_page_template(self):
        """Return custom HTML template with side-by-side layout."""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>{{ model_name }}</title>
    <link rel="stylesheet" href="/static/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/external/d3/d3.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        #header {
            background-color: #2c3e50;
            color: white;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
        }
        #controls {
            text-align: right;
            margin-bottom: 20px;
        }
        #controls button {
            margin-left: 10px;
            padding: 8px 20px;
            font-size: 14px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            background-color: #3498db;
            color: white;
        }
        #controls button:hover {
            background-color: #2980b9;
        }
        #viz-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        .viz-element {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        #stats-container {
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
            font-size: 16px;
            font-weight: bold;
            color: #2c3e50;
        }
        #fps-slider {
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div id="header">
        <h1>{{ model_name }}</h1>
        <div id="controls">
            <label>Frames Per Second: <span id="fps-display">3</span></label>
            <input type="range" id="fps-slider" min="1" max="20" value="3" step="1">
            <button onclick="reset()" id="reset-button">Reset</button>
            <button onclick="step()" id="step-button">Step</button>
            <button onclick="toggleRun()" id="play-button">Start</button>
        </div>
    </div>
    
    <div id="viz-container">
        <div class="viz-element" id="chart-element"></div>
        <div class="viz-element" id="network-element"></div>
    </div>
    
    <div id="stats-container"></div>

    <script src="/static/external/jquery/jquery.min.js"></script>
    <script src="/static/js/runcontrol.js"></script>
    <script src="/static/external/d3/d3.min.js"></script>
    <script src="/static/js/CanvasModule.js"></script>
    <script src="/static/js/NetworkModule_d3.js"></script>
    <script src="/static/js/ChartModule.js"></script>
    
    <script>
        var model_params = {{ model_params|tojson }};
        var ws = null;
        var running = false;
        var currentStep = 0;
        
        // Connect to WebSocket
        function connectSocket() {
            var ws_url = "ws://{{ host }}:{{ port }}/ws";
            ws = new WebSocket(ws_url);
            
            ws.onopen = function() {
                console.log("WebSocket connected");
                reset();
            };
            
            ws.onmessage = function(message) {
                var msg = JSON.parse(message.data);
                if (msg.type === "viz_state") {
                    renderVisualization(msg.data);
                }
            };
        }
        
        function renderVisualization(data) {
            // Render chart (index 0)
            if (data[0]) {
                document.getElementById("chart-element").innerHTML = data[0];
            }
            // Render network (index 1)
            if (data[1]) {
                document.getElementById("network-element").innerHTML = data[1];
            }
            // Render stats (index 2)
            if (data[2]) {
                document.getElementById("stats-container").innerHTML = data[2];
            }
        }
        
        function reset() {
            ws.send(JSON.stringify({"type": "reset"}));
            currentStep = 0;
            running = false;
            document.getElementById("play-button").textContent = "Start";
        }
        
        function step() {
            ws.send(JSON.stringify({"type": "get_step", "step": currentStep + 1}));
            currentStep++;
        }
        
        function toggleRun() {
            running = !running;
            document.getElementById("play-button").textContent = running ? "Pause" : "Start";
            if (running) {
                runModel();
            }
        }
        
        function runModel() {
            if (running) {
                step();
                var fps = parseInt(document.getElementById("fps-slider").value);
                setTimeout(runModel, 1000 / fps);
            }
        }
        
        document.getElementById("fps-slider").oninput = function() {
            document.getElementById("fps-display").textContent = this.value;
        };
        
        connectSocket();
    </script>
</body>
</html>
"""


def run_server():
    """Run the custom server with side-by-side layout."""
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
    
    # Stats text panel (BOTTOM)
    stats = StatsElement()
    
    server = CustomModularServer(
        CyberRangeModel,
        [chart, net, stats],
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
    
    # Override the page handler to use custom template
    import tornado.web
    
    class CustomPageHandler(tornado.web.RequestHandler):
        def get(self):
            self.render_string(server.get_page_template(), 
                             model_name=server.model_name,
                             model_params=server.model_kwargs,
                             host="127.0.0.1",
                             port=server.port)
    
    server.launch()


if __name__ == "__main__":
    run_server()
