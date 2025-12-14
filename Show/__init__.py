# ComfyUI/custom_nodes/Show/__init__.py

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
    CATEGORY = "Debug"
    OUTPUT_NODE = True

    def show_text(self, string):
        return {"ui": {"string": [string]}, "result": (string,)}

NODE_CLASS_MAPPINGS = {"Show": Show}
NODE_DISPLAY_NAME_MAPPINGS = {"Show": "⚙️Show"}

WEB_DIRECTORY = "web"
