# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import sys

from ..core import CATEGORY

class RvLogic_Float:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("FLOAT", {
                    "default": 1.00,
                    "min": -sys.float_info.max,
                    "max": sys.float_info.max,
                    "step": 0.01,
                    "tooltip": "Float value to output."
                }),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PRIMITIVE.value
    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("float",)

    FUNCTION = "execute"

    def execute(self, value):
        # Outputs a float value for logic operations or workflow branching.
        # Handles None and empty input robustly.
        # Type safety: ensure valid float
        
        if not isinstance(value, (float, int)):
            value = 1.0
        return (float(value),)

NODE_NAME = 'Float [RvTools-X]'
NODE_DESC = 'Float'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvLogic_Float
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}