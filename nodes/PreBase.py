# ComfyUI/custom_nodes/ComfyRage/nodes/PreBase.py

import random
import re


class PreBase:
    """Shared processing logic for Pre and PreShow."""

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
        # Single-pass stack-based expansion
        stack = []
        result = []
        i = 0
        while i < len(string):
            char = string[i]
            if char == '{':
                # Find the matching closing brace
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
                # Split by | at depth 0
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

                choice = rng.choice(parts) if parts else ""
                result.append(choice)
                i = j
            else:
                result.append(char)
                i += 1
        return "".join(result)

    def clean_commas(self, line):
        if not line or line.isspace():
            return ""

        # 1. Remove double/triple commas
        line = re.sub(r",{2,}", ",", line)

        # 2. Remove commas before closing brackets/parens
        line = re.sub(r",\s*([\)\]])", r"\1", line)

        # 3. Remove commas after opening brackets/parens
        line = re.sub(r"([\(\[])\s*,", r"\1", line)

        # 4. Trim leading/trailing whitespace and commas
        line = line.strip().strip(',')

        return line if line else ""

    def cleanup(self, string):
        lines = []
        for line in string.splitlines():
            cleaned = self.clean_commas(line)
            if cleaned:
                lines.append(cleaned)

        if not lines:
            return ""

        # Join lines with commas, ensuring no double commas at join points
        # We don't need to strip/add commas per line if we join carefully
        result_parts = []
        for line in lines:
            # If the line already ends with a structural char (like |), don't add comma
            if line.endswith('|') or line.endswith('AND'):
                result_parts.append(line)
            else:
                result_parts.append(line + ",")

        # Join with newlines, then remove any trailing comma from the very last line
        final_string = "\n".join(result_parts)
        return final_string.rstrip(',')

    def clean_weight_groups(self, string):
        if not string:
            return ""
        # Simplified: just ensure no empty groups or weird spacing
        string = re.sub(r"\(\s*\)", "", string)
        string = re.sub(r"\(\s*:\s*[0-9.]+\s*\)", "", string)
        string = re.sub(r"\(\s*,\s*", "(", string)
        string = re.sub(r"\(\s*([^()]+?)\s*:\s*([0-9.]+)\s*\)", lambda m: f"({m.group(1).strip()}:{m.group(2)})", string)
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
            else:
                current_segment += char
        if current_segment:
            segments.append((current_segment, depth))

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
