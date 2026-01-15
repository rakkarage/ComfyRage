# ComfyUI/custom_nodes/ComfyRage/__init__.py

import os

from .nodes.Pre import Pre
from .nodes.Show import Show
from .nodes.Debug import Debug
from .nodes.Notify import Notify

NODE_CLASS_MAPPINGS = {
    "Pre": Pre,
    "Show": Show,
    "Debug": Debug,
    "Notify": Notify,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Pre": "⚙️Pre",
    "Show": "👁️Show",
    "Debug": "🐞Debug",
    "Notify": "🔔Notify",
}

WEB_DIRECTORY = os.path.join(os.path.dirname(__file__), "web")

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
