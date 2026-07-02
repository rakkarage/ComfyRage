# ComfyUI/custom_nodes/ComfyRage/nodes/Show.py
from .Util import extract


class Show:
    """Display text persistently. Optionally forward input."""

    @staticmethod
    def INPUT_TYPES():
        return {
            "required": {},
            "optional": {"string": ("STRING", {})},
        }

    RETURN_TYPES = ("STRING",)
    INPUT_IS_LIST = True
    OUTPUT_NODE = True
    FUNCTION = "run"
    CATEGORY = "rage"

    def run(self, **kwargs):
        values = extract(kwargs)
        return {
            "ui": {"processed": values or [""]},
            "result": (", ".join(values or []),),
        }
