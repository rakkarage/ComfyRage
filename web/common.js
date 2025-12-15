// ComfyUI/custom_nodes/ComfyRage/web/common.js

export class ComfyRageCommon {
    static createDisplayExtension(nodeName) {
        return {
            name: `ComfyRage.${nodeName}.Display`,
            async beforeRegisterNodeDef(nodeType, nodeData) {
                if (nodeData.name === nodeName) {
                    // Add a widget definition to the node
                    if (!nodeData.input) nodeData.input = {};
                    if (!nodeData.input.required) nodeData.input.required = {};
                    nodeData.input.required.text = ["STRING", { multiline: true }];

                    const onNodeCreated = nodeType.prototype.onNodeCreated;
                    const onExecuted = nodeType.prototype.onExecuted;

                    nodeType.prototype.onNodeCreated = function () {
                        onNodeCreated?.apply(this, arguments);

                        // Create the readonly text area
                        if (this.widgets) {
                            const pos = this.widgets.findIndex((w) => w.name === "text");
                            if (pos !== -1) {
                                const widget = this.widgets[pos];
                                widget.inputEl.readOnly = true;
                                widget.inputEl.style.color = "#AAA";
                                widget.inputEl.style.opacity = 0.6;

                                // Store reference
                                this._displayWidget = widget;
                            }
                        }
                    };

                    nodeType.prototype.onExecuted = function (message) {
                        onExecuted?.apply(this, arguments);

                        const text = message?.text?.[0] ?? "";

                        // Update widget value
                        if (this._displayWidget) {
                            this._displayWidget.value = text;

                            // Also update the serialized value
                            const widgetIndex = this.widgets.findIndex(w => w === this._displayWidget);
                            if (widgetIndex !== -1 && this.widgets_values) {
                                this.widgets_values[widgetIndex] = text;
                            }
                        }
                    };
                }
            }
        };
    }
}
