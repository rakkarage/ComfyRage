# ComfyUI/custom_nodes/ComfyRage/nodes/Pre.py

import random, re

class Pre:
    @staticmethod
    def INPUT_TYPES():
        return {
            "required":{
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "display": ("STRING", {"multiline": True, "default": "(((tiger), bobcat), cat), {dog, {leash|}|rabbit|horse|fox|bird}, [simple_background] // Pre strips comments, expands random, and expands de-emphasis, Show + Debug proves it!"})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    CATEGORY = "text"

    def remove_comments(self, display):
        return re.sub(r'/\*.*?\*/|//[^\n\r]*', '', display, flags=re.DOTALL)

    def expand_random(self, seed, display):
        random.seed(seed)

        if display.count('{') != display.count('}'):
            raise ValueError("Unbalanced { } in input string")

        def find_brace_block(s):
            start = s.find('{')
            if start == -1:
                return None

            depth = 0
            for i in range(start, len(s)):
                if s[i] == '{':
                    depth += 1
                elif s[i] == '}':
                    depth -= 1
                    if depth == 0:
                        return (start, i)

            return None

        while True:
            block = find_brace_block(display)
            if not block:
                break

            start, end = block
            inner = display[start+1:end]

            parts = []
            buf = ""
            depth = 0
            for ch in inner:
                if ch == '{':
                    depth += 1
                    buf += ch
                elif ch == '}':
                    depth -= 1
                    buf += ch
                elif ch == '|' and depth == 0:
                    parts.append(buf.strip())
                    buf = ""
                else:
                    buf += ch
            parts.append(buf.strip())

            choice = random.choice(parts) if parts else ""
            display = display[:start] + choice + display[end+1:]

        return display

    def clean_commas(self, line):
        if not line or line.isspace():
            return ""

        while True:
            new_line = re.sub(r',\s*,', ',', line)
            if new_line == line:
                break
            line = new_line

        line = re.sub(r',\s*([\)\]])', r'\1', line)
        line = re.sub(r'^\s*,', '', line)
        line = re.sub(r'([\(\[])\s*,', r'\1', line)
        line = line.strip()

        if line == ',' or not line:
            return ""

        return line

    def cleanup(self, display):
        lines = []
        for line in display.splitlines():
            line = line.strip()
            if not line:
                continue

            line = self.clean_commas(line)
            if line:
                line = re.sub(r',\s*$', '', line).rstrip()
                lines.append(line)

        if not lines:
            return ""

        result = []
        for i, line in enumerate(lines):
            if i < len(lines) - 1 and line:
                line = line + ','
            result.append(line)

        return '\n'.join(result)

    def apply_deemphasis(self, display):
        result = []
        i = 0
        while i < len(display):
            if display[i] == '[':
                depth = 1
                j = i + 1
                while j < len(display) and depth > 0:
                    if display[j] == '[':
                        depth += 1
                    elif display[j] == ']':
                        depth -= 1
                    j += 1

                if depth == 0:
                    inner = display[i+1:j-1].strip()
                    nesting_depth = display[:i].count('[') - display[:i].count(']')

                    weight = 0.9 ** (nesting_depth + 1)
                    weight_str = str(weight).rstrip("0").rstrip(".")
                    result.append(f"({inner}:{weight_str})")
                    i = j
                else:
                    result.append(display[i])
                    i += 1
            else:
                result.append(display[i])
                i += 1

        return ''.join(result)

    def run(self, seed, display):
        stripped = self.remove_comments(display)
        expanded = self.expand_random(seed, stripped)
        cleaned = self.cleanup(expanded)
        final = self.apply_deemphasis(cleaned)

        return (final,)

NODE_CLASS_MAPPINGS = { "Pre": Pre }
NODE_DISPLAY_NAME_MAPPINGS = { "Pre": "⚙️Pre" }
