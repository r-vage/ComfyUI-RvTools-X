# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import re
from ..core import CATEGORY

class RvText_ReplaceString:
    CATEGORY = CATEGORY.MAIN.value + CATEGORY.TEXT.value
    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "String": ("STRING", {"default": "", "tooltip": "Input string to process."}),
                "Regex": ("STRING", {"default": "", "tooltip": "Regular expression pattern to match."}),
                "ReplaceWith": ("STRING", {"default": "", "tooltip": "Replacement string for matches."}),
            }
        }

    def execute(self, String: str, Regex: str, ReplaceWith: str) -> tuple[str]:
        # Replace substrings in String using Regex, then remove line breaks for prompt output.
        replaced = re.sub(Regex, ReplaceWith, String)
        replaced = re.sub(r"[\r\n]+", " ", replaced)
        return (replaced,)

NODE_NAME = 'Replace String [RvTools-X]'
NODE_DESC = 'Replace String'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvText_ReplaceString
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}