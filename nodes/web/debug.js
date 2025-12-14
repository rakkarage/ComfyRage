// ComfyUI/custom_nodes/ComfyRage/nodes/web/show.js

import { app } from "../../scripts/app.js";
import { ComfyRageCommon } from "./Common.js";

app.registerExtension({
    name: "ComfyRage.Debug",

    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "Debug") {
            ComfyRageCommon.log("Debug", "Setting up UI");

            // Store original methods
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            const onExecuted = nodeType.prototype.onExecuted;
            const onConfigure = nodeType.prototype.onConfigure;
            const configure = nodeType.prototype.configure;
            const serialize = nodeType.prototype.serialize;

            // Store text independently
            let currentText = "";
            let displayWidget = null;

            // Function to create/update the widget using Common.js
            function createWidget(text = "") {
                ComfyRageCommon.log("Debug", `createWidget() with: "${text.substring(0, 50)}${text.length > 50 ? '...' : ''}"`);

                // Create widget using shared utility
                displayWidget = ComfyRageCommon.createOutputWidget(this, text, {
                    name: "output"
                });

                // Store for easy access
                this._displayWidget = displayWidget;
                currentText = text;

                // Resize using shared utility
                ComfyRageCommon.resizeNode(this);

                return displayWidget;
            }

            // 1. OVERRIDE configure() - This receives the saved data
            nodeType.prototype.configure = function (data) {
                ComfyRageCommon.log("Debug", `configure() called with data:`, data);

                // Store saved text using shared utility
                currentText = ComfyRageCommon.getTextFromState(this, data);
                ComfyRageCommon.log("Debug", `Saved text found in configure(): "${currentText.substring(0, 50)}${currentText.length > 50 ? '...' : ''}"`);

                // Call original configure
                const ret = configure?.apply(this, arguments);

                return ret;
            };

            // 2. CREATE WIDGET (but wait for configure to load saved text)
            nodeType.prototype.onNodeCreated = function () {
                const ret = onNodeCreated?.apply(this, arguments);

                ComfyRageCommon.log("Debug", `onNodeCreated - currentText: "${currentText.substring(0, 50)}${currentText.length > 50 ? '...' : ''}"`);

                // Create widget with currentText (empty or saved)
                createWidget.call(this, currentText);

                return ret;
            };

            // 3. LOAD SAVED STATE - OLD WAY (backup)
            nodeType.prototype.onConfigure = function () {
                const ret = onConfigure?.apply(this, arguments);

                ComfyRageCommon.log("Debug", `onConfigure - widgets_values:`, this.widgets_values);
                ComfyRageCommon.log("Debug", `onConfigure - currentText: "${currentText}"`);

                // Update widget with saved text if we have it
                if (currentText && displayWidget) {
                    ComfyRageCommon.log("Debug", `Updating widget with saved text: "${currentText.substring(0, 50)}${currentText.length > 50 ? '...' : ''}"`);
                    displayWidget.value = currentText;
                }

                return ret;
            };

            // 4. UPDATE ON EXECUTION
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);

                const text = message?.string?.[0] ?? "";
                ComfyRageCommon.log("Show", `onExecuted received: "${text.substring(0, 50)}${text.length > 50 ? '...' : ''}"`);

                currentText = text;

                if (displayWidget) {
                    displayWidget.value = text;
                } else {
                    createWidget.call(this, text);
                }
            };

            // 5. OVERRIDE serialize() to save our text using shared utility
            nodeType.prototype.serialize = function () {
                // Call original serialize
                const result = serialize ? serialize.apply(this, arguments) : {};

                // Save current text using shared utility
                const savedResult = ComfyRageCommon.saveTextToState(this, currentText, result);
                ComfyRageCommon.log("Debug", `serialize() saving: "${currentText.substring(0, 50)}${currentText.length > 50 ? '...' : ''}"`);

                return savedResult;
            };

            ComfyRageCommon.log("Debug", "Extension registered");
        }
    }
});
