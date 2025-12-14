"""
ComfyUI/custom_nodes/ComfyRage/__init__.py
"""

import os

# Initialize
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
WEB_DIRECTORY = None

# 1. Load Show (package with web)
try:
    from .Show import (
        NODE_CLASS_MAPPINGS as show_map,
        NODE_DISPLAY_NAME_MAPPINGS as show_disp,
        WEB_DIRECTORY as show_web
    )
    NODE_CLASS_MAPPINGS.update(show_map)
    NODE_DISPLAY_NAME_MAPPINGS.update(show_disp)
    WEB_DIRECTORY = show_web
    print(f"Loaded Show: {list(show_map.keys())}")
except ImportError as e:
    print(f"Warning: Could not load Show: {e}")

# 2. Load Debug.py
try:
    # Use relative import
    from .Debug import (
        NODE_CLASS_MAPPINGS as debug_map,
        NODE_DISPLAY_NAME_MAPPINGS as debug_disp
    )
    NODE_CLASS_MAPPINGS.update(debug_map)
    NODE_DISPLAY_NAME_MAPPINGS.update(debug_disp)
    print(f"Loaded Debug: {list(debug_map.keys())}")
except ImportError as e:
    print(f"Warning: Could not load Debug: {e}")

# 3. Load Pre.py
try:
    from .Pre import (
        NODE_CLASS_MAPPINGS as pre_map,
        NODE_DISPLAY_NAME_MAPPINGS as pre_disp
    )
    NODE_CLASS_MAPPINGS.update(pre_map)
    NODE_DISPLAY_NAME_MAPPINGS.update(pre_disp)
    print(f"Loaded Pre: {list(pre_map.keys())}")
except ImportError as e:
    print(f"Warning: Could not load Pre: {e}")

print(f"Total nodes registered: {len(NODE_CLASS_MAPPINGS)}")

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']