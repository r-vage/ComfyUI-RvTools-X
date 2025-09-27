# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY

class RvLogic_String:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("STRING", {"default": "", "tooltip": "String value to output."}),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PRIMITIVE.value
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)

    FUNCTION = "execute"

    def execute(self, value=""):
        # Outputs a string value for logic operations or workflow branching.
        # Handles None and empty input robustly.
        #
        # Type safety: ensure valid string
        if not isinstance(value, str):
            value = ""
        return (value,)

NODE_NAME = 'String [RvTools-X]'
NODE_DESC = 'String'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvLogic_String
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}