# ComfyUI/custom_nodes/ComfyRage/nodes/Pre.py

import random, re


class Pre:
    @staticmethod
    def INPUT_TYPES():
        EXAMPLE_TEXT = "({cat, {collar|}|dog, {collar|leash, ({viewer_holding_leash|})|}, {bone||}}), [[ornate_border], simple_background] // test"
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
                "string": (
                    "STRING",
                    {
                        "multiline": True,
                        "placeholder": EXAMPLE_TEXT,
                        "default": EXAMPLE_TEXT,
                    },
                ),
            }
        }

    RETURN_TYPES = ("STRING",)
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
            inner = string[start + 1 : end]

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
            string = string[:start] + choice + string[end + 1 :]

        return string

    def clean_commas(self, line):
        if not line or line.isspace():
            return ""

        while True:
            new_line = re.sub(r",\s*,", ",", line)
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

    def apply_deemphasis(self, string):
        # Process brackets from innermost to outermost
        while True:
            # Find innermost bracket pair
            start = -1
            end = -1
            depth = 0
            max_depth = 0

            # First, find the deepest nesting level
            for i, char in enumerate(string):
                if char == "[":
                    depth += 1
                    if depth > max_depth:
                        max_depth = depth
                        start = i
                elif char == "]":
                    depth -= 1
                    if depth == max_depth - 1 and start != -1:
                        end = i
                        break

            if start == -1 or end == -1:
                break

            # Extract the innermost bracket content
            inner = string[start + 1 : end].strip()

            # Calculate weight based on nesting depth
            # Each bracket level multiplies by 0.9
            # Innermost (depth = max_depth) gets 0.9
            # Next level gets 0.9 × 0.9 = 0.81, etc.
            weight = 0.9 ** (max_depth)

            # Format weight string
            weight_str = f"{weight:.10f}".rstrip("0").rstrip(".")

            # Replace the bracket with weighted parentheses
            replacement = f"({inner}:{weight_str})"
            string = string[:start] + replacement + string[end + 1 :]

        return string

    def run(self, seed, string):
        stripped = self.remove_comments(string)
        expanded = self.expand_random(seed, stripped)
        cleaned = self.cleanup(expanded)
        final = self.apply_deemphasis(cleaned)

        return (final,)
