# ComfyUI/custom_nodes/ComfyRage/nodes/PreBase.py

import random
import re


class PreBase:
    """Shared processing logic for Pre and PreShow: strip comments, expand random choices, clean up commas, and apply emphasis."""

    EXAMPLE_TEXT = "({cat, {collar|}|dog, {collar|leash, ({viewer_holding_leash|})|}, {bone||}}), [[ornate_border], simple_background] // test"

    FUNCTION = "run"
    CATEGORY = "rage"

    @staticmethod
    def INPUT_TYPES():
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
                "pre": ("STRING", {"multiline": True, "placeholder": PreBase.EXAMPLE_TEXT, "default": PreBase.EXAMPLE_TEXT}),
            },
        }

    def remove_comments(self, string):
        return re.sub(r"/\*.*?\*/|//[^\n\r]*", "", string, flags=re.DOTALL)

    def expand_random(self, seed, string):
        rng = random.Random(seed)

        if string.count("{") != string.count("}"):
            raise ValueError("Unbalanced { } in input.")
        if string.count("[") != string.count("]"):
            raise ValueError("Unbalanced [ ] in input.")
        if string.count("(") != string.count(")"):
            raise ValueError("Unbalanced ( ) in input.")

        return self._expand_recursive(rng, string)

    def _expand_recursive(self, rng, string):
        result = []
        i = 0
        while i < len(string):
            char = string[i]
            if char == '{':
                depth = 1
                j = i + 1
                while j < len(string) and depth > 0:
                    if string[j] == '{':
                        depth += 1
                    elif string[j] == '}':
                        depth -= 1
                    j += 1

                if depth != 0:
                    raise ValueError("Unbalanced { } in input.")

                inner = string[i+1:j-1]
                parts = []
                buf = ""
                d = 0
                for c in inner:
                    if c == '{':
                        d += 1
                        buf += c
                    elif c == '}':
                        d -= 1
                        buf += c
                    elif c == '|' and d == 0:
                        parts.append(buf.strip())
                        buf = ""
                    else:
                        buf += c
                parts.append(buf.strip())

                if len(parts) <= 1:
                    raise ValueError(f"Invalid random block '{{{inner}}}': must contain at least one '|' to separate choices.")

                choice = rng.choice(parts) if parts else ""

                result.append(self._expand_recursive(rng, choice))
                i = j
            else:
                result.append(char)
                i += 1
        return "".join(result)

    def clean_commas(self, line):
        if not line or line.isspace():
            return ""

        parts = [part.strip() for part in line.split(",")]
        parts = [part for part in parts if part]

        if not parts:
            return ""

        return ", ".join(parts)

    def cleanup(self, string):
        lines = []
        for line in string.splitlines():
            line = line.strip()
            if not line:
                continue
            line = self.clean_commas(line)
            if line:
                line = re.sub(r",\s*$", "", line).rstrip()
                line = re.sub(r" +", " ", line)
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

        depth = 0
        for char in string:
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
                if depth < 0:
                    raise ValueError("Unbalanced ( ) in input.")
        if depth != 0:
            raise ValueError("Unbalanced ( ) in input.")

        for _ in range(20):
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
                if depth < 0:
                    raise ValueError("Unbalanced [ ] in input.")
            else:
                current_segment += char
        if current_segment:
            segments.append((current_segment, depth))

        if depth != 0:
            raise ValueError("Unbalanced [ ] in input.")

        result = ""
        for text, d in segments:
            if d > 0 and text.strip():
                match = re.match(r"^(.*?):([0-9.]+)$", text.strip())
                if match:
                    inner_text, existing_weight = match.groups()
                    final_weight = float(existing_weight) * (0.9 ** d)
                else:
                    inner_text = text.strip()
                    final_weight = 0.9 ** d

                weight_str = f"{final_weight:.4f}".rstrip("0").rstrip(".")
                result += f"({inner_text}:{weight_str})"
            else:
                result += text
        return result

    def process(self, seed, pre):
        result = self.remove_comments(pre)
        result = self.expand_random(seed, result)
        result = self.apply_deemphasis(result)
        result = self.clean_weight_groups(result)
        return self.cleanup(result)
