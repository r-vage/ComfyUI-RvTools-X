# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from __future__ import annotations
from ..core import CATEGORY, purge_vram
from ..core import AnyType

any = AnyType("*")

class RvSwitch_Multi_Any:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "inputcount": ("INT", {"default": 2, "min": 1, "max": 64, "step": 1, "tooltip": "Number of ANY inputs to expose; click 'Update inputs' to add or remove inputs."}),
                "Purge_VRAM": ("BOOLEAN", {"default": False, "tooltip": "If enabled, purges VRAM before switching."}),
            },
            "optional": {
                "any_1": (any, {"tooltip": "Any input #1 (highest priority). Leave empty to bypass."}),
                "any_2": (any, {"tooltip": "Any input #2 (used if #1 is empty)."}),
            }
        }

    RETURN_TYPES = (any,)
    RETURN_NAMES = ("*",)
    FUNCTION = "select"
    CATEGORY = CATEGORY.MAIN.value +  CATEGORY.MULTISWITCHES.value
    DESCRIPTION = "Multi-switch for ANY inputs. Click 'Update inputs' (frontend) to add/remove any_X inputs." 

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
            if isinstance(v, str) and v.strip() == "":
                return True
            return False

        for i in range(1, max(1, inputcount) + 1):
            key = f"any_{i}"
            val = kwargs.get(key)
            if not _is_empty(val):
                return (val,)

        raise RuntimeError(f"RvSwitch_Multi_Any: no value found among any_1..any_{inputcount}.")

NODE_NAME = 'Any Multi-Switch [RvTools-X]'
NODE_DESC = 'Any Multi-Switch'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvSwitch_Multi_Any
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
