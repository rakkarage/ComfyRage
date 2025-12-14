# ComfyUI/custom_nodes/ComfyRage/nodes/Pre.py

import random, re

class Pre:
    @staticmethod
    def INPUT_TYPES():
        return {
            "required":{
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "string": ("STRING", {"multiline": True, "default": "{dog, {leash|}|cat|horse}, [simple_background] // Pre strips comments, expands random, and expands de-emphasis, Show + Debug proves it!"})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "process"
    CATEGORY = "text"

    def remove_comments(self, string):
        return re.sub(r'/\*.*?\*/|//.*$', '', string, flags=re.DOTALL | re.MULTILINE)

    def expand_random(self, seed, string):
        random.seed(seed)

        if string.count('{') != string.count('}'):
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

            return None  # unbalanced

        # Expand blocks from innermost → outermost until none left
        while True:
            block = find_brace_block(string)
            if not block:
                break

            start, end = block
            inner = string[start+1:end]

            # Split by top-level | (only at depth 0)
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
            string = string[:start] + choice + string[end+1:]

        return string

    def cleanup(self, string):
        cleaned_lines = []
        for line in string.splitlines():
            line = line.strip()

            # collapse repeated commas
            line = re.sub(r'\s*,\s*,+', ',', line)

            # collapse blank entries
            while ',,' in line or ', ,' in line:
                line = re.sub(r',\s*,', ',', line)

            # remove commas before closing brackets/parens
            line = re.sub(r',\s*\)', ')', line)
            line = re.sub(r',\s*\]', ']', line)

            # remove empty item at start of brackets/parens
            line = re.sub(r'\[\s*,\s*', '[', line)
            line = re.sub(r'\(\s*,\s*', '(', line)

            # remove leading commas/spaces
            line = re.sub(r'^[\s,]+', '', line)

            # compress trailing commas/spaces → exactly one comma
            line = re.sub(r'[\s,]+$', ',', line)

            if line == ',':
                line = ''

            if line:
                cleaned_lines.append(line)

        return '\n'.join(cleaned_lines)

    def apply_deemphasis(self, string):
        result = []
        i = 0
        while i < len(string):
            if string[i] == '[':
                # Find matching closing bracket
                depth = 1
                j = i + 1
                while j < len(string) and depth > 0:
                    if string[j] == '[':
                        depth += 1
                    elif string[j] == ']':
                        depth -= 1
                    j += 1

                if depth == 0:
                    # Extract inner content (between [ and ])
                    inner = string[i+1:j-1].strip()
                    # Count nesting: how many unmatched [ are before this position
                    nesting_depth = string[:i].count('[') - string[:i].count(']')

                    weight = 0.9 ** (nesting_depth + 1)
                    weight_str = str(weight).rstrip("0").rstrip(".")
                    result.append(f"({inner}:{weight_str})")
                    i = j
                else:
                    result.append(string[i])
                    i += 1
            else:
                result.append(string[i])
                i += 1

        return ''.join(result)

    def process(self, seed, string):
        stripped = self.remove_comments(string)
        expanded = self.expand_random(seed, stripped)
        cleaned = self.cleanup(expanded)
        final = self.apply_deemphasis(cleaned)

        return (final,)

NODE_CLASS_MAPPINGS = { "Pre": Pre }
NODE_DISPLAY_NAME_MAPPINGS = { "Pre": "⚙️Pre" }
