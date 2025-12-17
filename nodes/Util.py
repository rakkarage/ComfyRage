# ComfyUI/custom_nodes/ComfyRage/nodes/Util.py

import json

class AlwaysEqualProxy(str):
    def __eq__(self, _):
        return True

    def __ne__(self, _):
        return False

any_type = AlwaysEqualProxy("*")

def extract(kwargs):
    values = []

    if "anything" not in kwargs:
        return values

    for val in kwargs["anything"]:
        try:
            if isinstance(val, str):
                values.append(val)
            elif isinstance(val, (int, float, bool)):
                values.append(str(val))
            else:
                values.append(json.dumps(val, indent=4))
        except Exception:
            values.append(str(val))

    return values

def inject(values, unique_id, extra_pnginfo):
    if not extra_pnginfo:
        return

    info = extra_pnginfo[0]
    if not isinstance(info, dict) or "workflow" not in info:
        return

    workflow = info["workflow"]
    node = next(
        (x for x in workflow["nodes"] if str(x["id"]) == unique_id[0]),
        None
    )

    if node:
        node["widgets_values"] = [values]
