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
def inject(values, unique_id, extra_pnginfo, keep=0):
    if not extra_pnginfo:
        return

    # extra_pnginfo is a dict, but arrives wrapped in a list when the
    # calling node sets INPUT_IS_LIST=True (all inputs, including hidden
    # ones, get list-wrapped in that case). Handle both.
    info = extra_pnginfo[0] if isinstance(extra_pnginfo, (list, tuple)) else extra_pnginfo
    if not isinstance(info, dict):
        return

    workflow = info.get("workflow")
    if not workflow or "nodes" not in workflow:
        return

    # unique_id is passed as a string by ComfyUI (not a list) when
    # the node doesn't set INPUT_IS_LIST. Handle both cases.
    uid = unique_id[0] if isinstance(unique_id, (list, tuple)) else unique_id

    node = next((x for x in workflow["nodes"] if str(x["id"]) == str(uid)), None)
    if node:
        # keep=0 (default): replace widgets_values entirely -- correct for
        # nodes like Show/Debug with no real widgets ahead of the display
        # one. keep=N: preserve the first N entries (e.g. PreShow's
        # seed/control_after_generate/pre) instead of overwriting them.
        existing = node.get("widgets_values") or []
        node["widgets_values"] = list(existing[:keep]) + [values]
