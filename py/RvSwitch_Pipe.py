# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, cstr, purge_vram
from typing import Any, Dict, Tuple

class RvSwitch_Pipe:
    CATEGORY = CATEGORY.MAIN.value + CATEGORY.SWITCHES.value
    RETURN_TYPES = ("pipe",)
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 2, "tooltip": "Select which pipe input to output (1 or 2)."}),
                "Purge_VRAM": ("BOOLEAN", {"default": False, "tooltip": "If True, purges VRAM before switching."}),
            },
            "optional": {
                "pipe1": ("pipe", {"tooltip": "First pipe input."}),
                "pipe2": ("pipe", {"tooltip": "Second pipe input."}),
            }
        }

    def execute(self, Input: int, Purge_VRAM: bool, pipe1: Any = None, pipe2: Any = None) -> Tuple[Any]:
        if Purge_VRAM:
            purge_vram()

        if Input == 1:
            return (pipe1,)
        else:
            return (pipe2,)

NODE_NAME = 'Pipe Switch [RvTools-X]'
NODE_DESC = 'Pipe Switch'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvSwitch_Pipe
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
