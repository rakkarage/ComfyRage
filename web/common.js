// ComfyUI/custom_nodes/ComfyRage/web/common.js

import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

export class ComfyRageCommon {
    static createDisplayExtension(nodeName) {
        return {
            name: `ComfyRage.${nodeName}.Display`,
            async beforeRegisterNodeDef(nodeType, nodeData) {
                if (nodeData.name !== nodeName) return;

                // Reusable populate function (copied from Easy-Use)
                function populate(text, name = 'text') {
                    // Remove all widgets from 'name' onward
                    if (this.widgets) {
                        const pos = this.widgets.findIndex(w => w.name === name);
                        if (pos !== -1) {
                            for (let i = pos; i < this.widgets.length; i++) {
                                this.widgets[i].onRemove?.();
                            }
                            this.widgets.length = pos;
                        }
                    }

                    // Create one read-only widget per line (text is expected to be an array)
                    let lines = Array.isArray(text) ? text : [text];
                    for (const line of lines) {
                        const w = ComfyWidgets.STRING(this, name, ["STRING", { multiline: true }], app).widget;
                        w.inputEl.readOnly = true;
                        w.inputEl.style.opacity = 0.6;
                        w.value = line;
                    }

                    // Auto-resize node
                    requestAnimationFrame(() => {
                        const sz = this.computeSize();
                        if (sz[0] < this.size[0]) sz[0] = this.size[0];
                        if (sz[1] < this.size[1]) sz[1] = this.size[1];
                        this.onResize?.(sz);
                        app.graph.setDirtyCanvas(true, false);
                    });
                }

                // On execution: update display
                const onExecuted = nodeType.prototype.onExecuted;
                nodeType.prototype.onExecuted = function (message) {
                    onExecuted?.apply(this, arguments);
                    if (message?.text !== undefined) {
                        // Easy-Use expects message.text to be an ARRAY (even for single value)
                        let display = Array.isArray(message.text) ? message.text : [message.text];
                        populate.call(this, display, 'text');
                    }
                };

                // On load: restore from widgets_values
                const onConfigure = nodeType.prototype.onConfigure;
                nodeType.prototype.onConfigure = function () {
                    onConfigure?.apply(this, arguments);
                    if (this.widgets_values?.length) {
                        // widgets_values is [ ["line1", "line2"] ] or ["single"]
                        let values = this.widgets_values[0];
                        if (!Array.isArray(values)) values = [values];
                        populate.call(this, values, 'text');
                    }
                };

                // On serialize: save current widget values
                const serialize = nodeType.prototype.serialize;
                nodeType.prototype.serialize = function () {
                    const orig = serialize ? serialize.apply(this, arguments) : {};
                    // Collect all 'text' widget values
                    const textWidgets = this.widgets?.filter(w => w.name === 'text') || [];
                    const values = textWidgets.map(w => w.value);
                    return { ...orig, widgets_values: [values] }; // Save as [["text"]] like Easy-Use
                };
            }
        };
    }
}
