// ComfyUI/custom_nodes/ComfyRage/web/common.js

import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

export class ComfyRageCommon {
    static getWidgetInput(widget) {
        const inputEl = widget?.element ?? widget?.inputEl;
        if (inputEl?.tagName === "TEXTAREA" || inputEl?.tagName === "INPUT") return inputEl;
        return inputEl?.querySelector?.("textarea, input") ?? null;
    }

    static setWidgetReadonly(widget, value) {
        const inputEl = ComfyRageCommon.getWidgetInput(widget);
        widget.options = { ...widget.options, read_only: true };
        widget.comfyRageReadonlyValue = value;
        if (!inputEl) return;

        inputEl.readOnly = true;
        inputEl.setAttribute("readonly", "readonly");
    }

    static createDisplayExtension(nodeName) {
        return {
            name: `ComfyRage.${nodeName}.Display`,
            async beforeRegisterNodeDef(nodeType, nodeData) {
                if (nodeData.name !== nodeName) return;

                function populate(text, name = 'value') {
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
                        const inputData = ["STRING", { multiline: true, placeholder: "No input.", read_only: true }];
                        const w = ComfyWidgets.STRING(this, name, inputData, app).widget;
                        w.value = line;
                        ComfyRageCommon.setWidgetReadonly(w, line);
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
                        populate.call(this, message.text, 'value');
                    }
                };

                const onConfigure = nodeType.prototype.onConfigure;
                nodeType.prototype.onConfigure = function () {
                    onConfigure?.apply(this, arguments);
                    if (this.widgets_values?.length) {
                        populate.call(this, this.widgets_values[0], 'value');
                    }
                };

                const serialize = nodeType.prototype.serialize;
                nodeType.prototype.serialize = function () {
                    const orig = serialize ? serialize.apply(this, arguments) : {};
                    const textWidgets = this.widgets?.filter(w => w.name === 'value') || [];
                    return { ...orig, widgets_values: [textWidgets.map(w => w.value)] };
                };
            }
        };
    }
}