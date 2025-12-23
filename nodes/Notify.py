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
    CATEGORY = "util"

    def run(self, **kwargs):
        return {"ui": {"text": ""}, "result": ()}


NODE_CLASS_MAPPINGS = {"Notify": Notify}
NODE_DISPLAY_NAME_MAPPINGS = {"Notify": "⚙️Notify"}
