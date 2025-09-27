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
                "string": ("STRING", {"multiline": True, "default": ""}, "Multiline string input.\nSplits into a list of lines and returns the full string joined by commas.\nUseful for prompt construction, text processing, or passing lists to downstream nodes."),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.TEXT.value
    RETURN_TYPES = ("STRING","STRING",)
    RETURN_NAMES = ("string", "string_list",)

    OUTPUT_IS_LIST = (False, True)

    FUNCTION = "execute"

    def execute(self, string=None):
        # Outputs the input multiline string as a single joined string and as a list of lines.
        # Handles None, empty, and whitespace-only input robustly.
        if not isinstance(string, str) or not string or string.isspace():
            return ("", [""])

        # Strip and split the input
        string = string.strip()
        string_list = string.split('\n')

        # Filter out empty lines and strip whitespace
        string_list = [line.strip() for line in string_list if line.strip()]

        # If no valid lines found, return empty
        if not string_list:
            return ("", [""])

        # Output: fallback for single item
        if len(string_list) == 1:
            return (string_list[0], string_list)
        joined_string = " ".join(string_list)
        return (joined_string, string_list)

NODE_NAME = 'String Multiline with List [RvTools-X]'
NODE_DESC = 'String Multiline with List'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvText_Multiline
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}