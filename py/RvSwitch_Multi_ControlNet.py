# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from __future__ import annotations
from ..core import CATEGORY, purge_vram

class RvSwitch_Multi_ControlNet:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "inputcount": ("INT", {"default": 2, "min": 1, "max": 64, "step": 1, "tooltip": "Number of CONTROLNET inputs to expose; click 'Update inputs' to add or remove inputs."}),
                "Purge_VRAM": ("BOOLEAN", {"default": False, "tooltip": "If enabled, purges VRAM before switching."}),
            },
            "optional": {
                "controlnet_1": ("CONTROL_NET", {"tooltip": "ControlNet input #1 (highest priority). Leave empty to bypass."}),
                "controlnet_2": ("CONTROL_NET", {"tooltip": "ControlNet input #2 (used if #1 is empty)."}),
            }
        }

    RETURN_TYPES = ("CONTROL_NET",)
    RETURN_NAMES = ("controlnet",)
    FUNCTION = "select"
    CATEGORY = CATEGORY.MAIN.value +  CATEGORY.MULTISWITCHES.value
    DESCRIPTION = "Multi-switch for CONTROL_NET inputs. Click 'Update inputs' (frontend) to add/remove controlnet_X inputs."

    def select(self, inputcount, Purge_VRAM=False, **kwargs):
        if Purge_VRAM:
            purge_vram()

        def _is_empty(v):
            if v is None:
                return True
            if isinstance(v, (tuple, list)) and len(v) == 0:
                return True
            if isinstance(v, dict) and len(v) == 0:
                return True
            return False

        for i in range(1, max(1, inputcount) + 1):
            key = f"controlnet_{i}"
            val = kwargs.get(key)
            if not _is_empty(val):
                return (val,)

        raise RuntimeError(f"RvSwitch_Multi_ControlNet: no controlnet found among controlnet_1..controlnet_{inputcount}.")

NODE_NAME = 'ControlNet Multi-Switch [RvTools-X]'
NODE_DESC = 'ControlNet Multi-Switch'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvSwitch_Multi_ControlNet
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
