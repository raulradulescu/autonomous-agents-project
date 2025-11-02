"""Simple custom server with side-by-side layout using a custom template."""
from __future__ import annotations

import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import json

from mesa.visualization.modules import ChartModule, NetworkModule
from ..model.cyber_range import CyberRangeModel
from ..viz.network import network_portrayal
from ..viz.stats import StatsElement


class SocketHandler(tornado.websocket.WebSocketHandler):
    """WebSocket handler for model updates."""
    
    def open(self):
        print("WebSocket opened")
        self.model = None
        
    def on_message(self, message):
        msg = json.loads(message)
        
        if msg["type"] == "reset":
            # Create new model
            self.model = CyberRangeModel(
                num_nodes=20,
                k=4,
                p=0.15,
                num_attackers=2,
                num_defenders=3,
                num_users=10,
                attacker_skill=0.55,
                defender_diligence=0.65,
                user_click_prob=0.25,
                seed=42,
            )
            self.send_state()
            
        elif msg["type"] == "get_step":
            if self.model:
                self.model.step()
                self.send_state()
    
    def send_state(self):
        """Send current model state to client."""
        if not self.model:
            return
            
        # Get network portrayal
        network_data = network_portrayal(self.model.G)
        
        # Get datacollector data for chart
        df = self.model.datacollector.get_model_vars_dataframe()
        chart_data = []
        if not df.empty:
            for col in ['healthy', 'compromised', 'patched', 'quarantined']:
                chart_data.append({
                    'name': col,
                    'data': df[col].tolist() if col in df.columns else []
                })
        
        # Get stats text
        healthy = sum(1 for _, v in self.model.G.nodes(data=True) if v["state"] == "healthy")
        compromised = sum(1 for _, v in self.model.G.nodes(data=True) if v["state"] == "compromised")
        patched = sum(1 for _, v in self.model.G.nodes(data=True) if v["state"] == "patched")
        quarantined = sum(1 for _, v in self.model.G.nodes(data=True) if v["state"] == "quarantined")
        stats_text = f"Step: {self.model.step_count} | Healthy: {healthy} | Compromised: {compromised} | Patched: {patched} | Quarantined: {quarantined}"
        
        self.write_message(json.dumps({
            'type': 'state',
            'network': network_data,
            'chart': chart_data,
            'stats': stats_text,
            'step': self.model.step_count
        }))


class MainHandler(tornado.web.RequestHandler):
    """Main page handler."""
    
    def get(self):
        self.render("index.html")


def make_app():
    """Create the Tornado application."""
    # Get the template directory
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/ws", SocketHandler),
    ], template_path=template_dir)


def run_server():
    """Run the custom server."""
    app = make_app()
    app.listen(8555)
    print("Interface starting at http://127.0.0.1:8555")
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run_server()
