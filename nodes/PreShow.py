# ComfyUI/custom_nodes/ComfyRage/nodes/PreShow.py

from .PreBase import PreBase
from .Util import inject


class PreShow(PreBase):
    """Strip comments, expand random choices, clean up commas, and apply emphasis to the input string. Displays result persistently."""

    @staticmethod
    def INPUT_TYPES():
        types = PreBase.INPUT_TYPES()
        types["hidden"] = {"unique_id": "UNIQUE_ID", "extra_pnginfo": "EXTRA_PNGINFO"}
        return types

    OUTPUT_NODE = True

    def run(self, seed, pre, unique_id=None, extra_pnginfo=None):
        result = self.process(seed, pre)
        if unique_id and extra_pnginfo:
            # keep=3: preserve seed, ComfyUI's auto-added
            # control_after_generate, and pre -- confirmed via saved
            # workflow JSON. Only the trailing display entry is replaced.
            inject(result, unique_id, extra_pnginfo, keep=3)
        return {
            "ui": {"processed": [result] if result else [""]},
            "result": (seed, result)
        }
