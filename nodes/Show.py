# ComfyUI/custom_nodes/ComfyRage/nodes/Show.py

from .Util import any_type, extract, inject

class Show:
    @staticmethod
    def INPUT_TYPES():
        return {
            "required": {},
            "optional": {"anything": (any_type, {}),},
            "hidden": {"unique_id": "UNIQUE_ID", "extra_pnginfo": "EXTRA_PNGINFO",}
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ('output',)
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

        if len(values) == 1:
            return { "ui": {"text": values}, "result": (values[0],), }
        else:
            return { "ui": {"text": values}, "result": (values,), }

NODE_CLASS_MAPPINGS = {"Show": Show}
NODE_DISPLAY_NAME_MAPPINGS = {"Show": "⚙️Show"}
