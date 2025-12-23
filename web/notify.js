// ComfyUI/custom_nodes/ComfyRage/web/notify.js

import { app } from "../../scripts/app.js";

export const playSound = (file, volume) => {
    if (!file) {
        file = 'notify.mp3'
    }
    if (!(file.startsWith('http') || file.startsWith('https'))) {
        if (!file.includes('/')) {
            file = 'assets/' + file
        }
        file = new URL(file, import.meta.url)
    }
    const url = new URL(file)
    const audio = new Audio(url)
    audio.volume = volume
    audio.play()
}

const NAME = "Notify";

app.registerExtension({
    name: NAME,
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name === NAME) {
            const oldOnExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = async function () {
                oldOnExecuted?.apply(this, arguments);
                playSound("notify.mp3", 0.5);
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
