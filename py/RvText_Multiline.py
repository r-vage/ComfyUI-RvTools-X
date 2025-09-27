# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY

class RvText_Multiline:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"multiline": True, "default": ""}, "Multiline string input.\nOutputs the string as-is.\nUseful for prompt construction, text processing, or passing text to downstream nodes."),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.TEXT.value
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)

    FUNCTION = "execute"

    def execute(self, string=""):
        if not isinstance(string, str) or not string:
            return ("",)
        return (string,)

NODE_NAME = 'String Multiline [RvTools-X]'
NODE_DESC = 'String Multiline'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvText_Multiline
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}