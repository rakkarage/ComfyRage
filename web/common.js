// ComfyUI/custom_nodes/ComfyRage/web/common.js

import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

export class ComfyRageCommon {
  static getWidgetInput(widget) {
    const inputEl = widget?.element ?? widget?.inputEl;
    if (inputEl?.tagName === "TEXTAREA" || inputEl?.tagName === "INPUT")
      return inputEl;
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

        function populate(text, name = "processed") {
          if (this.widgets) {
            const toRemove = this.widgets.filter((w) => w.name === name);
            for (const w of toRemove) w.onRemove?.();
            this.widgets = this.widgets.filter((w) => w.name !== name);
          }

          for (const line of text) {
            const inputData = [
              "STRING",
              { multiline: true, placeholder: "No input.", read_only: true },
            ];
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
          if (message?.processed !== undefined) {
            populate.call(this, message.processed, "processed");
          }
        };

        const onConfigure = nodeType.prototype.onConfigure;
        nodeType.prototype.onConfigure = function () {
          onConfigure?.apply(this, arguments);
          if (!this.widgets_values?.length) return;

          // The "processed" widget doesn't exist yet at this point (it's created
          // below by populate()), so widgets_values here is just the real widgets
          // unless a previous run's display text was saved too. Bail if not.
          const knownWidgetCount = (this.widgets ?? []).filter(
            (w) => w.name !== "processed",
          ).length;
          if (this.widgets_values.length <= knownWidgetCount) return;

          const saved = this.widgets_values[this.widgets_values.length - 1];
          if (saved !== undefined) {
            populate.call(
              this,
              Array.isArray(saved) ? saved : [saved],
              "processed",
            );
          }
        };
      },
    };
  }
}
