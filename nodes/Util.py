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
