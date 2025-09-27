# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, cstr, purge_vram
from typing import Any, Dict, Tuple

class RvSwitch_Guider:
    CATEGORY = CATEGORY.MAIN.value + CATEGORY.SWITCHES.value
    RETURN_TYPES = ("GUIDER",)
    RETURN_NAMES = ("guider",)
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2, "tooltip": "Select which GUIDER input to output (1 or 2)."}),
                "Purge_VRAM": ("BOOLEAN", {"default": False, "tooltip": "If True, purges VRAM before switching."}),
            },
            "optional": {
                "input1": ("GUIDER", {"forceInput": True, "tooltip": "First GUIDER input."}),
                "input2": ("GUIDER", {"forceInput": True, "tooltip": "Second GUIDER input."}),
            }
        }

    def execute(self, Input: int, Purge_VRAM: bool, input1: Any = None, input2: Any = None) -> Tuple[Any]:

        if Purge_VRAM:
            purge_vram()    

        if Input == 1:
            return (input1,)
        else:
            return (input2,)

    @classmethod
    def VALIDATE_INPUTS(cls, Input: int) -> bool:
        return True

NODE_NAME = 'Guider Switch [RvTools-X]'
NODE_DESC = 'Guider Switch'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvSwitch_Guider
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
