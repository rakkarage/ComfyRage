// ComfyUI/custom_nodes/Show/web/index.js

import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

app.registerExtension({
    name: "Show.Display",

    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "Show") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            const onExecuted = nodeType.prototype.onExecuted;
            const onConfigure = nodeType.prototype.onConfigure;
            const configure = nodeType.prototype.configure;  // Get original configure
            const serialize = nodeType.prototype.serialize;  // Get original serialize

            // Store text independently
            let currentText = "";

            // Function to create/update the widget
            function createWidget(text = "") {
                console.log("🔧 createWidget() with:", text);

                // Clear existing widget
                if (this.widgets) {
                    const pos = this.widgets.findIndex((w) => w.name === "output");
                    if (pos !== -1) {
                        this.widgets[pos].onRemove?.();
                        this.widgets.splice(pos, 1);
                    }
                }

                // Create new widget
                const w = ComfyWidgets["STRING"](this, "output",
                    ["STRING", { multiline: true }],
                    app
                ).widget;

                // Style it
                w.inputEl.readOnly = true;
                w.inputEl.style.color = "#AAA";
                w.inputEl.style.opacity = 0.6;
                w.inputEl.style.width = "100%";
                w.value = text;

                // Store for easy access
                this._displayWidget = w;
                currentText = text;

                // Resize
                requestAnimationFrame(() => {
                    const sz = this.computeSize();
                    if (sz[0] < this.size[0]) sz[0] = this.size[0];
                    if (sz[1] < this.size[1]) sz[1] = this.size[1];
                    this.onResize?.(sz);
                    app.graph.setDirtyCanvas(true, false);
                });

                return w;
            }

            // 1. OVERRIDE configure() - This receives the saved data
            nodeType.prototype.configure = function (data) {
                console.log("⚙️ configure() called with data:", data);

                // Store saved text BEFORE calling original configure
                if (data?.widgets_values && data.widgets_values.length > 0) {
                    currentText = data.widgets_values[0] || "";
                    console.log("📥 Saved text found in configure():", currentText);
                }

                // Call original configure
                const ret = configure?.apply(this, arguments);

                return ret;
            };

            // 2. CREATE WIDGET (but wait for configure to load saved text)
            nodeType.prototype.onNodeCreated = function () {
                const ret = onNodeCreated?.apply(this, arguments);

                console.log("🆕 onNodeCreated - currentText:", currentText);

                // Create widget with currentText (empty or saved)
                createWidget.call(this, currentText);

                return ret;
            };

            // 3. LOAD SAVED STATE - OLD WAY (backup)
            nodeType.prototype.onConfigure = function () {
                const ret = onConfigure?.apply(this, arguments);

                console.log("🔧 onConfigure - widgets_values:", this.widgets_values);
                console.log("🔧 onConfigure - currentText:", currentText);

                // Update widget with saved text if we have it
                if (currentText && this._displayWidget) {
                    console.log("🔄 Updating widget with saved text:", currentText);
                    this._displayWidget.value = currentText;
                }

                return ret;
            };

            // 4. UPDATE ON EXECUTION
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);

                const text = message?.string?.[0] ?? "";
                console.log("⚡ onExecuted received:", text);

                currentText = text;

                if (this._displayWidget) {
                    this._displayWidget.value = text;
                } else {
                    createWidget.call(this, text);
                }
            };

            // 5. OVERRIDE serialize() to save our text
            nodeType.prototype.serialize = function () {
                // Call original serialize
                const result = serialize ? serialize.apply(this, arguments) : {};

                // Ensure widgets_values exists
                if (!result.widgets_values) {
                    result.widgets_values = [];
                }

                // Save current text
                result.widgets_values[0] = currentText || "";
                console.log("💿 serialize() saving:", result.widgets_values[0]);

                return result;
            };

            console.log("✅ Show extension registered");
        }
    }
});