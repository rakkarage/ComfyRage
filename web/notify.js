// ComfyUI/custom_nodes/ComfyRage/web/notify.js

import { app } from "../../scripts/app.js";

export const playSound = (file = "assets/notify.mp3", volume = 1) => {
    const base = new URL(file, import.meta.url).toString();
    const url = `${base}?cachebuster=${Date.now()}_${Math.floor(Math.random() * 1000000)}`;
    const audio = new Audio(url);
    audio.volume = volume;
    audio.play()
};

const NAME = "Notify";

app.registerExtension({
    name: NAME,
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name === NAME) {
            const oldOnExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = async function () {
                oldOnExecuted?.apply(this, arguments);
                playSound();
                if (Notification.permission === "granted") {
                    new Notification("ComfyUI", { body: "Notify!" });
                } else if (Notification.permission !== "denied") {
                    await Notification.requestPermission();
                    if (Notification.permission === "granted") {
                        new Notification("ComfyUI", { body: "Notify!" });
                    }
                }
            };
        }
    },
});
