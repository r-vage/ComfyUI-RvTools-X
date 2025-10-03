// License: GNU General Public License v3.0
//
// This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
// See LICENSE file or <https://www.gnu.org/licenses/> for details.

import { app } from "../../../scripts/app.js";

// Robust dynamic inputs helper for RvTools multi-switch nodes
// - Uses explicit name prefixes that match the Python optional input names (int_, float_, string_, pipe_, any_, basicpipe_)
// - Ensures widget-only declared prefixed inputs get real sockets created so they are linkable
// - Adds/removes the highest-numbered prefixed entries when inputcount changes
// - Avoids duplicating sockets when a node already exposes optional inputs as widgets

app.registerExtension({
    name: "RvTools-X.DynamicInputs",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (!nodeData?.name) return;

        const multiNodes = {
            "RvSwitch_Multi_Model": { type: "MODEL", prefix: "model" },
            "Model Multi-Switch [RvTools-X]": { type: "MODEL", prefix: "model" },

            "RvSwitch_Multi_CLIP": { type: "CLIP", prefix: "clip" },
            "Clip Multi-Switch [RvTools-X]": { type: "CLIP", prefix: "clip" },

            "RvConversion_ConcatMulti": { type: "PIPE", prefix: "pipe" },
            "Concat Pipe Multi [RvTools-X]": { type: "PIPE", prefix: "pipe" },

            "RvSwitch_Multi_Latent": { type: "LATENT", prefix: "latent" },
            "Latent Multi-Switch [RvTools-X]": { type: "LATENT", prefix: "latent" },

            "RvSwitch_Multi_Vae": { type: "VAE", prefix: "vae" },
            "Vae Multi-Switch [RvTools-X]": { type: "VAE", prefix: "vae" },

            "RvSwitch_Multi_Conditioning": { type: "CONDITIONING", prefix: "conditioning" },
            "Conditioning Multi-Switch [RvTools-X]": { type: "CONDITIONING", prefix: "conditioning" },

            "RvSwitch_Multi_Image": { type: "IMAGE", prefix: "image" },
            "Image Multi-Switch [RvTools-X]": { type: "IMAGE", prefix: "image" },

            "RvSwitch_Multi_Images": { type: "IMAGES", prefix: "images" },
            "Images Multi-Switch [RvTools-X]": { type: "IMAGES", prefix: "images" },

            "RvSwitch_Multi_ControlNet": { type: "CONTROL_NET", prefix: "controlnet" },
            "ControlNet Multi-Switch [RvTools-X]": { type: "CONTROL_NET", prefix: "controlnet" },

            // Python uses lowercase 'pipe' in some nodes (ensure prefix matches python optional names)
            "RvSwitch_Multi_Pipe": { type: "pipe", prefix: "pipe" },
            "Pipe Multi-Switch [RvTools-X]": { type: "pipe", prefix: "pipe" },

            "RvSwitch_Multi_BasicPipe": { type: "BASIC_PIPE", prefix: "basicpipe" },
            "BasicPipe Multi-Switch [RvTools-X]": { type: "BASIC_PIPE", prefix: "basicpipe" },

            // Any uses special AnyType("*") in python; prefix 'any' matches python optional names
            "RvSwitch_Multi_Any": { type: "*", prefix: "any" },
            "Any Multi-Switch [RvTools-X]": { type: "*", prefix: "any" },

        };

        const baseName = nodeData.name && nodeData.name.includes('/') ? nodeData.name.split('/').pop() : nodeData.name;
        const info = multiNodes[baseName];
        if (!info) return;

        nodeType.prototype.onNodeCreated = function () {
            const node = this;

            // Helper to compute prefixed name
            const nameFor = (prefix, i) => `${prefix}_${i}`;

            const updateInputs = () => {
                if (!node.inputs) node.inputs = [];
                const w = node.widgets ? node.widgets.find(w => w.name === "inputcount") : null;
                const target = w ? w.value : 0;
                const prefix = info.prefix || (typeof info.type === 'string' ? info.type.toLowerCase() : 'input');

                // collect existing names
                const socketNames = new Set(node.inputs.filter(i => typeof i.name === 'string').map(i => i.name));
                const widgetNames = new Set((node.widgets || []).map(w => w.name).filter(n => typeof n === 'string'));
                const allExisting = new Set([...socketNames, ...widgetNames].filter(n => n.startsWith(prefix + '_')));

                // If counts match, just ensure widget-only names have sockets
                if (allExisting.size === target) {
                    for (let i = 1; i <= target; ++i) {
                        const nm = nameFor(prefix, i);
                        if (widgetNames.has(nm) && !socketNames.has(nm)) {
                            node.addInput(nm, info.type, info.shape !== undefined ? { shape: info.shape } : undefined);
                        }
                    }
                    return;
                }

                // If we need to reduce count, remove highest-numbered names first
                if (allExisting.size > target) {
                    const nums = Array.from(allExisting).map(n => {
                        const m = n.match(new RegExp(prefix + '_(\\d+)$'));
                        return m ? parseInt(m[1], 10) : null;
                    }).filter(Boolean).sort((a,b) => b - a);
                    for (const num of nums) {
                        if (allExisting.size <= target) break;
                        const nm = nameFor(prefix, num);
                        const si = node.inputs.findIndex(i => i.name === nm);
                        if (si !== -1) node.removeInput(si);
                        if (node.widgets) {
                            const wi = node.widgets.findIndex(w => w.name === nm);
                            if (wi !== -1) node.widgets.splice(wi, 1);
                        }
                        allExisting.delete(nm);
                    }
                    return;
                }

                // otherwise add missing sockets up to target
                for (let i = 1; i <= target; ++i) {
                    const nm = nameFor(prefix, i);
                    if (allExisting.has(nm)) continue;
                    node.addInput(nm, info.type, info.shape !== undefined ? { shape: info.shape } : undefined);
                    allExisting.add(nm);
                }
            };

            this.addWidget("button", "Update inputs", null, updateInputs);

            // quick initial update after a short delay to allow widgets to initialize
            setTimeout(() => { try { updateInputs(); } catch (e) {} }, 80);

            let last = null;
            const pollId = setInterval(() => {
                if (!node.widgets) return;
                const w = node.widgets.find(w => w.name === "inputcount");
                if (!w) return;
                if (w.value !== last) { last = w.value; updateInputs(); }
            }, 200);

            const origRemoved = this.onRemoved || function(){};
            this.onRemoved = function() { clearInterval(pollId); origRemoved.apply(this, arguments); };
        };
    }
});
