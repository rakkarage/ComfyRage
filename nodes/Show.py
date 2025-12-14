# ComfyUI/custom_nodes/ComfyRage/nodes/Show.py

class Show:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"multiline": True, "forceInput": True})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "show_text"
    CATEGORY = "text"
    OUTPUT_NODE = True

    def show_text(self, string):
        return {"ui": {"text": [string]}, "result": (string,)}

NODE_CLASS_MAPPINGS = {"Show": Show}
NODE_DISPLAY_NAME_MAPPINGS = {"Show": "⚙️Show"}
