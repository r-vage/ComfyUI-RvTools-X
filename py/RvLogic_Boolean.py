# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY

class RvLogic_Boolean:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("BOOLEAN", {"default": True, "tooltip": "Boolean value to output (True/False)."}),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PRIMITIVE.value
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("boolean",)

    FUNCTION = "execute"

    def execute(self, value=True):
        # Outputs a boolean value for logic operations or workflow branching.
        # Handles None and empty input robustly.
        # Type safety: ensure valid boolean
        if not isinstance(value, bool):
            value = True
        return (value,)

NODE_NAME = 'Boolean [RvTools-X]'
NODE_DESC = 'Boolean'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvLogic_Boolean
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}