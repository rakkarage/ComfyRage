# ComfyUI/custom_nodes/ComfyRage/nodes/Debug.py

import comfy.sd1_clip as sd1_clip
from .Util import extract, inject


class Debug:
    @staticmethod
    def INPUT_TYPES():
        return {
            "required": {},
            "optional": {"string": ("STRING", {})},
            "hidden": {"unique_id": "UNIQUE_ID", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ("STRING",)
    INPUT_IS_LIST = True
    OUTPUT_NODE = True
    FUNCTION = "run"
    CATEGORY = "text"

    def run(self, unique_id=None, extra_pnginfo=None, **kwargs):
        values = extract(kwargs)
        inject(values, unique_id, extra_pnginfo)

        if not values:
            return {"ui": {"text": []}, "result": ([],)}

        parsed_texts = []
        for val in values:
            weights = sd1_clip.token_weights(val, 1.0)
            parsed_texts.append(self.format_output(weights))

        return {"ui": {"text": [parsed_texts]}, "result": (values,)}

    def format_output(self, weights):
        if not weights:
            return ""

        lines = []

        for i, item in enumerate(weights):
            if isinstance(item, tuple):
                token, weight = item
                weight_str = f"{float(weight):.2f}"
                lines.append(f"{i:2d}. '{token}' (weight: {weight_str})")
            else:
                lines.append(f"{i:2d}. '{item}' (weight: 1.00)")

        return "\n".join(lines)


NODE_CLASS_MAPPINGS = {"Debug": Debug}
NODE_DISPLAY_NAME_MAPPINGS = {"Debug": "⚙️Debug"}
