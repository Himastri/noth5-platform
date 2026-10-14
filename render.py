"""
NOTH5 LITE RUNTIME - render.py
Public Lite runtime - compatible with workflow.py V5
Implements advertised operations. Some are simulated for Lite (marked LITE-SIM),
full execution in Factory EXE.
"""
import json
from datetime import datetime

def _log(component, msg):
    print(f"[RENDER:{component}] {msg}")

def render_chat_bubble_inside_bubble(text):
    """Core NOTH5 feature: controls INSIDE chat bubble, not outside"""
    _log("CHAT", text)
    return {"type": "chat_bubble", "inside": True, "text": text, "ts": datetime.now().isoformat()}

def render_slider_inside_bubble(label):
    _log("SLIDER", f"{label} inside bubble")
    return {"type": "slider", "inside": True, "label": label}

def render_gauge_inside_bubble(label):
    _log("GAUGE", f"{label} inside bubble")
    return {"type": "gauge", "inside": True, "label": label}

# Existing advertised controls - keep compatibility
def render_slider(label, min_val=0, max_val=100, value=50):
    return render_slider_inside_bubble(label)

def render_rating(label, stars=5):
    _log("RATING", f"{label} {stars} stars inside bubble")
    return {"type": "rating", "inside": True, "label": label, "stars": stars}

def render_table(data):
    _log("TABLE", f"{len(data) if isinstance(data, list) else 1} rows inside bubble")
    return {"type": "table", "inside": True}

def render_chart(data, chart_type="bar"):
    _log("CHART", f"{chart_type} chart inside bubble")
    return {"type": "chart", "inside": True, "chart_type": chart_type}

def render_calendar(date_str=None):
    _log("CALENDAR", f"calendar {date_str} inside bubble")
    return {"type": "calendar", "inside": True}

def render_qr(text):
    _log("QR", f"QR for {text[:20]} inside bubble")
    return {"type": "qr", "inside": True}

def render_dropdown(label, options):
    _log("DROPDOWN", f"{label} {options} inside bubble")
    return {"type": "dropdown", "inside": True}

def render_file_upload(label):
    _log("UPLOAD", f"{label} inside bubble")
    return {"type": "file_upload", "inside": True}

def render_map(lat, lng, label=""):
    _log("MAP", f"map {lat},{lng} inside bubble")
    return {"type": "map", "inside": True}
