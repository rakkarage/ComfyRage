# ComfyUI/custom_nodes/Pre.py

# ComfyUI only expands random variables that are in the actual clip text field, so if you pass the text into a subgraph that has random variables,
# it will not expand them. This node fixes that. You can also pass the putput to a show any/text node to display the expanded text.

# also remove c styles comments: `// line` and `/*block*/`

# also expands de-emphasis `[tag]` to `(tag:0.9)`

import random, re

class Pre:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required":{
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "text": ("STRING", {"multiline": True})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "process"
    CATEGORY = "Text"

    def remove_comments(self, text):
        def replacer(match):
            s = match.group(0)
            if s.startswith('/'):
                return ""
            else:
                return s
        pattern = re.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"', re.DOTALL | re.MULTILINE)
        return re.sub(pattern, replacer, text)

    def expand_random(self, seed, text):
        random.seed(seed)

        # Remove comments before expanding
        cleaned_text = self.remove_comments(text)

        if text.count('{') != text.count('}'):
            raise ValueError("Unbalanced { } in input text")

        def find_brace_block(s):
            """Finds the next balanced { ... } block, even multiline and nested."""
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

        # Expand blocks until none left
        while True:
            block = find_brace_block(text)
            if not block:
                break

            start, end = block
            inner = text[start+1:end]

            # Split by top-level |
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

        cleaned_lines = []
        for line in text.splitlines():
            line = line.strip()

            # collapse repeated commas
            line = re.sub(r'\s*,\s*,+', ',', line)

            # collapse blank entries
            while ',,' in line or ', ,' in line:
                line = re.sub(r',\s*,', ',', line)

            # NEW: remove commas before a closing parenthesis
            line = re.sub(r',\s*\)', ')', line)

            # NEW: remove commas before a closing bracket
            line = re.sub(r',\s*\]', ']', line)

            # remove empty item at start of bracketed list: "[, foo]" → "[foo]"
            line = re.sub(r'\[\s*,\s*', '[', line)

            # remove empty item at start of parenthesized list: "(, foo)" → "(foo)"
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
        # Common-sense mirror of () emphasis: 
        # ( ) depth N → 1.1^N
        # [ ] depth N → 0.9^N

        def replace_brackets(match):
            inner = match.group(1).strip()
            brackets = match.group(0)

            # count nesting depth: number of '[' at start
            depth = 0
            for c in brackets:
                if c == '[':
                    depth += 1
                else:
                    break

            weight = 0.9 ** depth
            w = str(weight).rstrip("0").rstrip(".")
            return f"({inner}:{w})"

        out = text

        # repeatedly process nested brackets from inside → out
        while True:
            new = re.sub(r'\[([^\[\]]+)\]', replace_brackets, out)
            if new == out:
                break
            out = new

        return out

    def process(self, seed, text):
        cleaned = self.remove_comments(text)
        expanded = self.expand_random(seed, cleaned)
        final = self.apply_deemphasis(expanded)
        return (final,)

NODE_CLASS_MAPPINGS = { "Pre": Pre }
NODE_DISPLAY_NAME_MAPPINGS = { "Pre": "⚙️Pre" }
