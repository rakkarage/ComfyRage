# ComfyUI/custom_nodes/ComfyRage/Debug.py

import comfy.sd1_clip as sd1_clip

class Debug:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("original", "parsed")
    FUNCTION = "parse"
    CATEGORY = "utils"

    def parse(self, text):
        try:
            weights = sd1_clip.token_weights(text, 1.0)
            parsed_text = self.format_output(weights)
        except Exception as e:
            parsed_text = f"Parse error: {str(e)}"

        return (text, parsed_text)

    def format_output(self, weights):
        if not weights:
            return "Empty prompt"

        lines = []
        for i, item in enumerate(weights):
            if isinstance(item, tuple):
                token, weight = item
                weight_str = f"{weight:.2f}" if isinstance(weight, float) else str(weight)
                lines.append(f"{i:2d}. '{token}' (weight: {weight_str})")
            else:
                lines.append(f"{i:2d}. '{item}' (weight: 1.00)")

        return "\n".join(lines)

NODE_CLASS_MAPPINGS = { "Debug": Debug }
NODE_DISPLAY_NAME_MAPPINGS = { "Debug": "⚙️Debug" }
