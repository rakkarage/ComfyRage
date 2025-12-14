# ComfyUI/custom_nodes/ComfyRage/nodes/Pre.py

import random, re

class Pre:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required":{
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "text": ("STRING", {"multiline": True, "default": "{dog, {leash|}|cat|horse}, [simple_background] // Pre strips comments, expands random, and expands de-emphasis, Show + Debug proves it!"})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "process"
    CATEGORY = "text"

    def remove_comments(self, text):
        return re.sub(r'/\*.*?\*/|//.*$', '', text, flags=re.DOTALL | re.MULTILINE)

    def expand_random(self, seed, text):
        random.seed(seed)

        if text.count('{') != text.count('}'):
            raise ValueError("Unbalanced { } in input text")

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
            block = find_brace_block(text)
            if not block:
                break

            start, end = block
            inner = text[start+1:end]

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
            text = text[:start] + choice + text[end+1:]

        return text

    def cleanup(self, text):
        cleaned_lines = []
        for line in text.splitlines():
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

    def apply_deemphasis(self, text):
        result = []
        i = 0
        while i < len(text):
            if text[i] == '[':
                # Find matching closing bracket
                depth = 1
                j = i + 1
                while j < len(text) and depth > 0:
                    if text[j] == '[':
                        depth += 1
                    elif text[j] == ']':
                        depth -= 1
                    j += 1

                if depth == 0:
                    # Extract inner content (between [ and ])
                    inner = text[i+1:j-1].strip()
                    # Count nesting: how many unmatched [ are before this position
                    nesting_depth = text[:i].count('[') - text[:i].count(']')

                    weight = 0.9 ** (nesting_depth + 1)
                    weight_str = str(weight).rstrip("0").rstrip(".")
                    result.append(f"({inner}:{weight_str})")
                    i = j
                else:
                    result.append(text[i])
                    i += 1
            else:
                result.append(text[i])
                i += 1

        return ''.join(result)

    def process(self, seed, text):
        cleaned = self.remove_comments(text)
        expanded = self.expand_random(seed, cleaned)
        cleanup = self.cleanup(expanded)
        final = self.apply_deemphasis(cleanup)

        return (final,)

NODE_CLASS_MAPPINGS = { "Pre": Pre }
NODE_DISPLAY_NAME_MAPPINGS = { "Pre": "⚙️Pre" }
