# ComfyUI/custom_nodes/ComfyRage/nodes/Notify.py

from .Util import AlwaysEqualProxy


class Notify:
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
