# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, cstr, purge_vram
from ..core import AnyType
from typing import Any, Dict, Tuple

any = AnyType("*")

class RvSwitch_IfExecute:
    CATEGORY = CATEGORY.MAIN.value + CATEGORY.SWITCHES.value
    RETURN_TYPES = (any,)
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        return {
            "required": {
                "on_true": (any, {"tooltip": "Value to return if boolean is True."}),
                "on_false": (any, {"tooltip": "Value to return if boolean is False."}),
                "boolean": ("BOOLEAN", {"forceInput": True, "tooltip": "Condition to select on_true or on_false."}),
                "Purge_VRAM": ("BOOLEAN", {"default": False, "tooltip": "If True, purges VRAM before switching."}),
            }
        }

    def execute(self, on_true: Any, on_false: Any, boolean: bool = True, Purge_VRAM: bool = False) -> Tuple[Any]:

        if Purge_VRAM:
            purge_vram()    
            
        if boolean:
            return (on_true,)
        else:
            return (on_false,)

NODE_NAME = 'IF A Else B [RvTools-X]'
NODE_DESC = 'IF A Else B'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvSwitch_IfExecute
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
