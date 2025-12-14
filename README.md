# ComfyRage

![Screenshot](screenshot.png)

```
{dog, {leash|}|cat|horse}, [simple_background] // Pre strips comments, expands random, and expands de-emphasis, Show + Debug proves it!
```

# Pre
- Strips comments: `/* comment1 */ tag1, tag2, // comment2`
- Expands random: `{tag1|tag2|etc}, {tag4|}`
- Expands de-emphasis: `[less[less]]`

Can use show or debug if you wanna see, or just pass to encoder.

# Show
- Shows text, optionally passes on input as output.

# Debug
- Show weights, optionally passes on input as output.

Thanks!