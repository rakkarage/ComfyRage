# ComfyUI/custom_nodes/ComfyRage/__init__.py

import os

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

from .nodes.Pre import (
    NODE_CLASS_MAPPINGS as pre_map,
    NODE_DISPLAY_NAME_MAPPINGS as pre_display_map,
)

NODE_CLASS_MAPPINGS.update(pre_map)
NODE_DISPLAY_NAME_MAPPINGS.update(pre_display_map)

from .nodes.Show import (
    NODE_CLASS_MAPPINGS as show_map,
    NODE_DISPLAY_NAME_MAPPINGS as show_display_map,
)

NODE_CLASS_MAPPINGS.update(show_map)
NODE_DISPLAY_NAME_MAPPINGS.update(show_display_map)

from .nodes.Debug import (
    NODE_CLASS_MAPPINGS as debug_map,
    NODE_DISPLAY_NAME_MAPPINGS as debug_display_map,
)

NODE_CLASS_MAPPINGS.update(debug_map)
NODE_DISPLAY_NAME_MAPPINGS.update(debug_display_map)

WEB_DIRECTORY = os.path.join(os.path.dirname(__file__), "web")

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
