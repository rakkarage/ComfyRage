# ComfyUI/custom_nodes/ComfyRage/__init__.py

import os

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

from .nodes.Pre import (
    NODE_CLASS_MAPPINGS as pre_map,
    NODE_DISPLAY_NAME_MAPPINGS as pre_name_map,
)

from .nodes.Show import (
    NODE_CLASS_MAPPINGS as show_map,
    NODE_DISPLAY_NAME_MAPPINGS as show_name_map,
)

from .nodes.Debug import (
    NODE_CLASS_MAPPINGS as debug_map,
    NODE_DISPLAY_NAME_MAPPINGS as debug_name_map,
)

from .nodes.Notify import (
    NODE_CLASS_MAPPINGS as notify_map,
    NODE_DISPLAY_NAME_MAPPINGS as notify_name_map,
)

NODE_CLASS_MAPPINGS |= pre_map | show_map | debug_map | notify_map
NODE_DISPLAY_NAME_MAPPINGS |= (
    pre_name_map | show_name_map | debug_name_map | notify_name_map
)

WEB_DIRECTORY = os.path.join(os.path.dirname(__file__), "web")

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
