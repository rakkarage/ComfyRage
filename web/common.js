// ComfyUI/custom_nodes/ComfyRage/web/common.js

import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

export class ComfyRageCommon {
    static createDisplayExtension(nodeName) {
        return {
            name: `ComfyRage.${nodeName}.Display`,
            async beforeRegisterNodeDef(nodeType, nodeData) {
                if (nodeData.name === nodeName) {
                    const { createOutputWidget, resizeNode, getTextFromState, saveTextToState } = ComfyRageCommon;

                    let currentText = "";
                    let displayWidget = null;

                    const onNodeCreated = nodeType.prototype.onNodeCreated;
                    const onExecuted = nodeType.prototype.onExecuted;
                    const onConfigure = nodeType.prototype.onConfigure;
                    const configure = nodeType.prototype.configure;
                    const serialize = nodeType.prototype.serialize;

                    nodeType.prototype.configure = function (data) {
                        currentText = getTextFromState(this, data);
                        return configure?.apply(this, arguments);
                    };

                    nodeType.prototype.onNodeCreated = function () {
                        onNodeCreated?.apply(this, arguments);
                        if (!displayWidget) {
                            displayWidget = createOutputWidget(this, currentText, { name: "output" });
                            resizeNode(this);
                        }
                    };

                    nodeType.prototype.onConfigure = function () {
                        onConfigure?.apply(this, arguments);
                        if (currentText && displayWidget) {
                            displayWidget.value = currentText;
                        }
                    };

                    nodeType.prototype.onExecuted = function (message) {
                        onExecuted?.apply(this, arguments);
                        const text = message?.text?.[0] ?? "";
                        currentText = text;
                        if (displayWidget) {
                            displayWidget.value = text;
                        }
                    };

                    nodeType.prototype.serialize = function () {
                        const result = serialize ? serialize.apply(this, arguments) : {};
                        return saveTextToState(this, currentText, result);
                    };
                }
            }
        };
    }

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

        if (node.widgets) {
            const pos = node.widgets.findIndex((w) => w.name === opts.name);
            if (pos !== -1) {
                node.widgets[pos].onRemove?.();
                node.widgets.splice(pos, 1);
            }
        }

        const w = ComfyWidgets["STRING"](node, opts.name,
            ["STRING", { multiline: opts.multiline }],
            app
        ).widget;

        if (opts.readonly) w.inputEl.readOnly = true;
        w.inputEl.style.color = opts.color;
        w.inputEl.style.opacity = opts.opacity;
        w.inputEl.style.width = opts.width;
        w.value = value;

        return w;
    }

    static resizeNode(node) {
        requestAnimationFrame(() => {
            const sz = node.computeSize();
            if (sz[0] < node.size[0]) sz[0] = node.size[0];
            if (sz[1] < node.size[1]) sz[1] = node.size[1];
            node.onResize?.(sz);
            app.graph.setDirtyCanvas(true, false);
        });
    }

    static saveTextToState(_node, text, result) {
        if (!result.widgets_values) {
            result.widgets_values = [];
        }
        result.widgets_values[0] = text || "";
        return result;
    }

    static getTextFromState(_node, data) {
        return data?.widgets_values?.[0] || "";
    }

    static log(component, ...args) {
        console.log(`[ComfyRage.${component}]`, ...args);
    }
}
