# ComfyUI/custom_nodes/ComfyRage/nodes/Pre.py

from .PreBase import PreBase


class Pre(PreBase):
    """Strip comments, expand random choices, clean up commas, and apply emphasis to the input string."""

    @staticmethod
    def INPUT_TYPES():
        return PreBase.INPUT_TYPES()

    def run(self, seed, pre):
        return (self.process(seed, pre),)
