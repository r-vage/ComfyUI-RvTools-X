# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import sys

from ..core import CATEGORY

class RvLogic_Integer:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("INT", {"default": 1, "min": -sys.maxsize, "max": sys.maxsize, "step": 1, "tooltip": "Integer value to output."}),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PRIMITIVE.value
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("int",)

    FUNCTION = "execute"

    def execute(self, value):
        # Outputs an integer value for logic operations or workflow branching.
        # Handles None and empty input robustly.
        # Type safety: ensure valid integer
        
        if not isinstance(value, int):
            value = 1
        return (int(value),)

NODE_NAME = 'Integer [RvTools-X]'
NODE_DESC = 'Integer'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvLogic_Integer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}