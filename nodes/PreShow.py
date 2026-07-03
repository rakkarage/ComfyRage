# ComfyUI/custom_nodes/ComfyRage/nodes/PreShow.py

from .PreBase import PreBase


class PreShow(PreBase):
    """Strip comments, expand random choices, clean up commas, and apply emphasis to the input string. Displays result persistently."""

    @staticmethod
    def INPUT_TYPES():
        return PreShow._input_types()

    RETURN_TYPES = ("STRING",)
    OUTPUT_NODE = True

    def run(self, seed, pre):
        result = self.process(seed, pre)
        return {
            "ui": {"processed": [result] if result else [""]},
            "result": (result,),
        }
