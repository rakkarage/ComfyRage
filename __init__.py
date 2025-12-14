"""
ComfyUI/custom_nodes/ComfyRage/__init__.py
"""
import os

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Import from nodes/ subdirectory
from .nodes.Show import NODE_CLASS_MAPPINGS as show_map
NODE_CLASS_MAPPINGS.update(show_map)

from .nodes.Debug import NODE_CLASS_MAPPINGS as debug_map
NODE_CLASS_MAPPINGS.update(debug_map)

from .nodes.Pre import NODE_CLASS_MAPPINGS as pre_map
NODE_CLASS_MAPPINGS.update(pre_map)

# Get WEB_DIRECTORY from Show (or whichever node has it)
try:
    from .nodes.Show import WEB_DIRECTORY
except ImportError:
    # Fallback: Construct path to nodes/web
    WEB_DIRECTORY = os.path.join(os.path.dirname(__file__), "nodes", "web")

print(f"[ComfyRage] Loaded {len(NODE_CLASS_MAPPINGS)} nodes")
print(f"[ComfyRage] Web directory: {WEB_DIRECTORY}")

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']