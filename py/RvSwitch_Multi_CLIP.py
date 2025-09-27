# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from __future__ import annotations
from ..core import CATEGORY, purge_vram

class RvSwitch_Multi_CLIP:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "inputcount": ("INT", {"default": 2, "min": 1, "max": 64, "step": 1, "tooltip": "Number of CLIP inputs to expose; click 'Update inputs' to add or remove inputs."}),
                "Purge_VRAM": ("BOOLEAN", {"default": False, "tooltip": "If enabled, purges VRAM and unloads all models before switching. Use when swapping large models to avoid OOM."}),
            },
            "optional": {
                "clip_1": ("CLIP", {"tooltip": "CLIP input #1 (highest priority). Leave empty to bypass."}),
                "clip_2": ("CLIP", {"tooltip": "CLIP input #2 (used if #1 is empty)."}),
            }
        }

    RETURN_TYPES = ("CLIP",)
    RETURN_NAMES = ("clip",)
    FUNCTION = "select"
    CATEGORY = CATEGORY.MAIN.value +  CATEGORY.MULTISWITCHES.value
    DESCRIPTION = "Multi-switch for CLIP inputs. Click 'Update inputs' (frontend) to add/remove clip_X inputs. The node returns the first connected/non-empty CLIP input."

    def select(self, inputcount, **kwargs):
        Purge_VRAM = kwargs.pop("Purge_VRAM", False)
        if Purge_VRAM:
            purge_vram()

        def _is_empty(v):
            if v is None:
                return True
            if isinstance(v, (tuple, list)) and len(v) == 0:
                return True
            if isinstance(v, (tuple, list)) and all(x is None for x in v):
                return True
            if isinstance(v, dict) and len(v) == 0:
                return True
            return False

        for i in range(1, max(1, inputcount) + 1):
            key = f"clip_{i}"
            val = kwargs.get(key)
            if not _is_empty(val):
                return (val,)

        raise RuntimeError(
            f"Clip Multi-Switch: no clip found among clip_1..clip_{inputcount}. "
            "Please connect at least one CLIP input or reduce inputcount."
        )

NODE_NAME = 'Clip Multi-Switch [RvTools-X]'
NODE_DESC = 'Clip Multi-Switch'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvSwitch_Multi_CLIP
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}