"""
ComfyUI Custom Nodes Aggregator
Automatically collects nodes from Show/, Debug.py, and Pre.py
"""

import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

# Initialize mappings
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
WEB_DIRECTORY = None

# List of modules to import
modules_to_load = [
    ("Show", "Show"),
    ("Debug.py", "Debug"),
    ("Pre.py", "Pre")
]

for module_path, module_name in modules_to_load:
    try:
        if module_name == "Show":
            # Import package
            from Show import (
                NODE_CLASS_MAPPINGS as mod_mappings,
                NODE_DISPLAY_NAME_MAPPINGS as mod_display,
                WEB_DIRECTORY as mod_web
            )
            WEB_DIRECTORY = mod_web  # Show sets the web directory
        else:
            # Import .py file
            if module_name == "Debug":
                import Debug as mod
            else:
                import Pre as mod
            
            mod_mappings = mod.NODE_CLASS_MAPPINGS
            mod_display = mod.NODE_DISPLAY_NAME_MAPPINGS
            mod_web = getattr(mod, 'WEB_DIRECTORY', None)
        
        # Update mappings
        NODE_CLASS_MAPPINGS.update(mod_mappings)
        NODE_DISPLAY_NAME_MAPPINGS.update(mod_display)
        
        print(f"✓ Loaded {module_name}: {list(mod_mappings.keys())}")
        
    except ImportError as e:
        print(f"✗ Failed to load {module_name}: {e}")
    except AttributeError as e:
        print(f"✗ {module_name} missing exports: {e}")

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']