// ComfyUI/custom_nodes/ComfyRage/web/common.js

import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

export class ComfyRageCommon {
    static createDisplayExtension(nodeName) {
        return {
            name: `ComfyRage.${nodeName}.Display`,
            async beforeRegisterNodeDef(nodeType, nodeData) {
                if (nodeData.name !== nodeName) return;

                function populate(text, name = 'text') {
                    if (this.widgets) {
                        const pos = this.widgets.findIndex(w => w.name === name);
                        if (pos !== -1) {
                            for (let i = pos; i < this.widgets.length; i++) {
                                this.widgets[i].onRemove?.();
                            }
                            this.widgets.length = pos;
                        }
                    }

                    for (const line of text) {
                        const w = ComfyWidgets.STRING(this, name, ["STRING", { multiline: true }], app).widget;
                        w.inputEl.readOnly = true;
                        w.inputEl.style.opacity = 0.6;
                        w.value = line;
                    }

                    requestAnimationFrame(() => {
                        const sz = this.computeSize();
                        if (sz[0] < this.size[0]) sz[0] = this.size[0];
                        if (sz[1] < this.size[1]) sz[1] = this.size[1];
                        this.onResize?.(sz);
                        app.graph.setDirtyCanvas(true, false);
                    });
                }

                const onExecuted = nodeType.prototype.onExecuted;
                nodeType.prototype.onExecuted = function (message) {
                    onExecuted?.apply(this, arguments);
                    if (message?.text !== undefined) {
                        populate.call(this, message.text, 'text');
                    }
                };

                const onConfigure = nodeType.prototype.onConfigure;
                nodeType.prototype.onConfigure = function () {
                    onConfigure?.apply(this, arguments);
                    if (this.widgets_values?.length) {
                        let values = this.widgets_values[0];
                        populate.call(this, values, 'text');
                    }
                };

                const serialize = nodeType.prototype.serialize;
                nodeType.prototype.serialize = function () {
                    const orig = serialize ? serialize.apply(this, arguments) : {};
                    const textWidgets = this.widgets?.filter(w => w.name === 'text') || [];
                    const values = textWidgets.map(w => w.value);
                    return { ...orig, widgets_values: [values] };
                };
            }
        };
    }
}
