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

ComfyUI normally only expands random prompt syntax in direct CLIP text inputs. When text is routed into multiple encoders (e.g., SDXL’s dual prompts) or through subgraphs, random syntax is **not expanded**.

The **Pre** node expands it once so the final text can be reliably viewed and reused.

**Features:**

- **Strip comments:** /* // */: `/* comment1 */ tag1, tag2, // comment2`
- **Expand random:** {|}: `{tag1|tag2|tag3, {tag4|}}`
- **Expand de-emphasis:** []: `[more[less]]`

You can combine **Pre** with **Show** or **Debug** to inspect the output, or pass the expanded text directly to an encoder.

### Show

ComfyUI does not include a way to display text in workflow.

**Features:**

- Shows text, optionally passes on input as output.

### Debug

ComfyUI does not include a way to see prompt weights.

**Features:**

- Show weights, optionally passes on input as output.
