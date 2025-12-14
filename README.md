# ComfyRage

## Example

![Screenshot](screenshot.png)

```
{dog, {leash|}|cat|horse}, [simple_background] // Pre strips comments, expands random, and expands de-emphasis, Show + Debug proves it!
```

## Install

Clone into `ComfyUI/custom_nodes`.

## Nodes

### Pre

ComfyUI only expands random prompt syntax if it’s written directly in a CLIP text input. Text coming from multiple encoders (e.g., SDXL’s dual prompts) or subgraphs is **not expanded**.

The **Pre** node expands it once so the final text can be reliably viewed, reused, and passed consistently to downstream nodes.

You can combine **Pre** with **Show** or **Debug** to inspect the output, or pass the expanded text directly to an encoder.

**Features:**

- **Strip comments:** /* // */: `/* comment1 */ tag1, tag2, // comment2`
- **Expand random:** {|}: `{tag1|tag2|tag3, {tag4|}}`
- **Expand de-emphasis:** []: `[more[less]]`

---

### Show

ComfyUI does not provide a built-in way to display the text as it flows through a workflow.

The **Show** node lets you **inspect the text** at any point, without modifying it, which is useful for debugging or verifying prompts.

**Features:**

- Shows text, optionally passes on input as output.

---

### Debug

ComfyUI does not provide a way to visualize weights, such as de-emphasis or nested weighting.

The **Debug** node lets you **inspect prompt weights** helping you understand how the final prompt will be interpreted by the encoder.

**Features:**

- Show weights, optionally passes on input as output.
