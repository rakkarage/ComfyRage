# ComfyRage

ComfyUI only expands random prompt syntax in direct CLIP text inputs. When the same text is routed into multiple encoders (such as SDXL’s dual prompts) or through subgraphs, the random syntax is left unexpanded. This node pre-expands it once so the final text can be viewed and reused reliably.

Install: clone into `ComfyUI/custom_nodes`. 

![Screenshot](screenshot.png)

```
{dog, {leash|}|cat|horse}, [simple_background] // Pre strips comments, expands random, and expands de-emphasis, Show + Debug proves it!
```

## Pre

- Strips comments /* // */: `/* comment1 */ tag1, tag2, // comment2`
- Expands random {|}: `{tag1|tag2|tag3, {tag4|}}`
- Expands de-emphasis []: `[more[less]]`

Can use show or debug if you wanna see, or just pass to encoder.

## Show

- Shows text, optionally passes on input as output.

## Debug

- Show weights, optionally passes on input as output.

Thanks!