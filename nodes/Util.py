# ComfyUI/custom_nodes/ComfyRage/nodes/Util.py


def extract(kwargs):
    if "string" not in kwargs:
        return []

    return [str(val) for val in kwargs["string"]]


def inject(values, unique_id, extra_pnginfo):
    if not extra_pnginfo:
        return

    info = extra_pnginfo[0]
    if not isinstance(info, dict) or "workflow" not in info:
        return

    workflow = info["workflow"]
    node = next((x for x in workflow["nodes"] if str(x["id"]) == unique_id[0]), None)

    if node:
        node["widgets_values"] = [values]
