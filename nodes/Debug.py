# ComfyUI/custom_nodes/ComfyRage/nodes/Debug.py

import comfy.sd1_clip as sd1_clip
from .Util import any_type, extract, inject

class Debug:
    @staticmethod
    def INPUT_TYPES():
        return {
            "required": {},
            "optional": {"anything": (any_type, {}),},
            "hidden": {"unique_id": "UNIQUE_ID", "extra_pnginfo": "EXTRA_PNGINFO",}
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
            parsed_text = "No input provided"
            return {"ui": {"text": [parsed_text]}, "result": ([],)}

        try:
            weights = sd1_clip.token_weights(values[0], 1.0)
            parsed_text = self.format_output(weights)
        except Exception as e:
            error_text = f"Input parse error: {str(e)}"
            all_parsed.append(error_text)

        return {"ui": {"text": [parsed_text]}, "result": (values[0],)}

    def format_output(self, weights):
        if not weights:
            return "Empty prompt"

        lines = []

        for i, item in enumerate(weights):
            if isinstance(item, tuple):
                token, weight = item
                weight_str = f"{float(weight):.2f}"
                lines.append(f"{i:2d}. '{token}' (weight: {weight_str})")
            else:
                lines.append(f"{i:2d}. '{item}' (weight: 1.00)")

        return "\n".join(lines)

NODE_CLASS_MAPPINGS = { "Debug": Debug }
NODE_DISPLAY_NAME_MAPPINGS = { "Debug": "⚙️Debug" }
