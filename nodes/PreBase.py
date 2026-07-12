# ComfyUI/custom_nodes/ComfyRage/nodes/PreBase.py

import random
import re


class PreBase:
    """Shared processing logic for Pre and PreShow: strip comments, expand random choices, clean up commas, and apply emphasis to the input string. Subclasses provide INPUT_TYPES/RETURN_TYPES/OUTPUT_NODE and run()."""

    EXAMPLE_TEXT = "({cat, {collar|}|dog, {collar|leash, ({viewer_holding_leash|})|}, {bone||}}), [[ornate_border], simple_background] // test"

    FUNCTION = "run"
    CATEGORY = "rage"

    def remove_comments(self, string):
        return re.sub(r"/\*.*?\*/|//[^\n\r]*", "", string, flags=re.DOTALL)

    def expand_random(self, seed, string):
        rng = random.Random(seed)

        if string.count("{") != string.count("}"):
            raise ValueError("Unbalanced { } in input.")

        def find_brace_block(s):
            start = s.find("{")
            if start == -1:
                return None

            depth = 0
            for i in range(start, len(s)):
                if s[i] == "{":
                    depth += 1
                elif s[i] == "}":
                    depth -= 1
                    if depth == 0:
                        return (start, i)

            return None

        while True:
            block = find_brace_block(string)
            if not block:
                break

            start, end = block
            inner = string[start + 1: end]

            parts = []
            buf = ""
            depth = 0
            for ch in inner:
                if ch == "{":
                    depth += 1
                    buf += ch
                elif ch == "}":
                    depth -= 1
                    buf += ch
                elif ch == "|" and depth == 0:
                    parts.append(buf.strip())
                    buf = ""
                else:
                    buf += ch
            parts.append(buf.strip())

            choice = rng.choice(parts) if parts else ""
            string = string[:start] + choice + string[end + 1:]

        return string

    def clean_commas(self, line):
        if not line or line.isspace():
            return ""

        while True:
            new_line = re.sub(r",\s*,\s*", ", ", line)
            if new_line == line:
                break
            line = new_line

        line = re.sub(r",\s*([\)\]])", r"\1", line)
        line = re.sub(r"^\s*,", "", line)
        line = re.sub(r"([\(\[])\s*,", r"\1", line)
        line = line.strip()

        if line == "," or not line:
            return ""

        return line

    def cleanup(self, string):
        lines = []
        for line in string.splitlines():
            line = line.strip()
            if not line:
                continue

            line = self.clean_commas(line)
            if line:
                line = re.sub(r",\s*$", "", line).rstrip()
                lines.append(line)

        if not lines:
            return ""

        result = []
        for i, line in enumerate(lines):
            if i < len(lines) - 1 and line:
                line = line + ","
            result.append(line)

        return "\n".join(result)

    def clean_weight_groups(self, string):
        if not string:
            return ""

        for _ in range(20):  # guard against pathological input
            new_string = re.sub(r"\(\s*\)", "", string)
            new_string = re.sub(r"\(\s*:\s*([0-9.]+)\s*\)", "", new_string)
            new_string = re.sub(r"\(\s*,\s*", "(", new_string)
            new_string = re.sub(r"\(\s*([^()]+?)\s*:\s*([0-9.]+)\s*\)",
                                lambda m: f"({m.group(1).strip()}:{m.group(2)})",
                                new_string)
            if new_string == string:
                return new_string
            string = new_string

        return string

    def apply_deemphasis(self, string):
        # Stack-based parser to calculate cumulative weights
        segments = []
        current_segment = ""
        depth = 0

        for char in string:
            if char == '[':
                if current_segment:
                    segments.append((current_segment, depth))
                    current_segment = ""
                depth += 1
            elif char == ']':
                if current_segment:
                    segments.append((current_segment, depth))
                    current_segment = ""
                depth -= 1
            else:
                current_segment += char

        if current_segment:
            segments.append((current_segment, depth))

        result = ""
        for text, d in segments:
            if d > 0 and text.strip():
                final_weight = 0.9 ** d
                weight_str = f"{final_weight:.10f}".rstrip("0").rstrip(".")
                result += f"({text.strip()}:{weight_str})"
            else:
                result += text

        return result

    def process(self, seed, pre):
        result = self.remove_comments(pre)
        result = self.expand_random(seed, result)
        result = self.apply_deemphasis(result)
        result = self.clean_weight_groups(result)
        return self.cleanup(result)

    @classmethod
    def _input_types(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF, "description": "Seed for random expansion. Use 0 for a random seed."}),
                "pre": (
                    "STRING",
                    {
                        "multiline": True,
                        "placeholder": cls.EXAMPLE_TEXT,
                        "default": cls.EXAMPLE_TEXT,
                        "description": "Input string to process. Supports comments, random choices, and emphasis.",
                    },
                ),
            },
        }
