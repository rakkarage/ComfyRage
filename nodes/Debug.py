# ComfyUI/custom_nodes/ComfyRage/nodes/Debug.py

import comfy.sd1_clip as sd1_clip

class Debug:
    @staticmethod
    def INPUT_TYPES():
        return {
            "required": {
                "string": ("STRING", {"multiline": True, "forceInput": True})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "parse"
    CATEGORY = "text"
    OUTPUT_NODE = True

    def parse(self, string):
        try:
            weights = sd1_clip.token_weights(string, 1.0)
            parsed_text = self.format_output(weights)
        except Exception as e:
            parsed_text = f"Parse error: {str(e)}"

        return {"ui": {"text": [parsed_text]}, "result": (string,)}

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
