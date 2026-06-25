# ComfyUI/custom_nodes/ComfyRage/nodes/Alert.py

from .Util import AlwaysEqualProxy


class Alert:
    """Display browser notification. Play sound."""

    @staticmethod
    def INPUT_TYPES():
        return {
            "required": {"any": (AlwaysEqualProxy("*"), {})},
        }

    OUTPUT_NODE = True
    RETURN_TYPES = tuple()
    FUNCTION = "run"
    CATEGORY = "rage"

    def run(self, **kwargs):
        return {"ui": {"text": ""}, "result": ()}
