// ComfyUI/custom_nodes/ComfyRage/web/common.js

import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

export class ComfyRageCommon {
    // Create a styled output text widget
    static createOutputWidget(node, value = "", options = {}) {
        const defaults = {
            name: "output",
            multiline: true,
            readonly: true,
            color: "#AAA",
            opacity: 0.6,
            width: "100%"
        };
        const opts = { ...defaults, ...options };

        // Clear existing widget if any
        if (node.widgets) {
            const pos = node.widgets.findIndex((w) => w.name === opts.name);
            if (pos !== -1) {
                node.widgets[pos].onRemove?.();
                node.widgets.splice(pos, 1);
            }
        }

        // Create new widget
        const w = ComfyWidgets["STRING"](node, opts.name,
            ["STRING", { multiline: opts.multiline }],
            app
        ).widget;

        // Style it
        if (opts.readonly) w.inputEl.readOnly = true;
        w.inputEl.style.color = opts.color;
        w.inputEl.style.opacity = opts.opacity;
        w.inputEl.style.width = opts.width;
        w.value = value;

        return w;
    }

    // Resize node to fit content
    static resizeNode(node) {
        requestAnimationFrame(() => {
            const sz = node.computeSize();
            if (sz[0] < node.size[0]) sz[0] = node.size[0];
            if (sz[1] < node.size[1]) sz[1] = node.size[1];
            node.onResize?.(sz);
            app.graph.setDirtyCanvas(true, false);
        });
    }

    // Save text to node state
    static saveTextToState(node, text, result) {
        if (!result.widgets_values) {
            result.widgets_values = [];
        }
        result.widgets_values[0] = text || "";
        return result;
    }

    // Get saved text from node state
    static getTextFromState(node, data) {
        return data?.widgets_values?.[0] || "";
    }

    // Logger with prefix
    static log(component, ...args) {
        console.log(`[ComfyRage.${component}]`, ...args);
    }
}
