# ComfyUI/custom_nodes/ComfyRage/nodes/Util.py


class AlwaysEqualProxy(str):
    def __eq__(self, _):
        return True

    def __ne__(self, _):
        return False


def extract(kwargs):
    if "string" not in kwargs:
        return []
    return [str(val) for val in kwargs["string"]]


# borrowed hack to save prompt into pnginfo for later retrieval
def inject(values, unique_id, extra_pnginfo):
    if not extra_pnginfo:
        return

    # extra_pnginfo is a dict, not a list
    if not isinstance(extra_pnginfo, dict):
        return

    workflow = extra_pnginfo.get("workflow")
    if not workflow or "nodes" not in workflow:
        return

    # unique_id is passed as a string by ComfyUI (not a list) when
    # the node doesn't set INPUT_IS_LIST. Handle both cases.
    uid = unique_id[0] if isinstance(unique_id, (list, tuple)) else unique_id

    node = next((x for x in workflow["nodes"] if str(x["id"]) == str(uid)), None)
    if node:
        node["widgets_values"] = [values]
