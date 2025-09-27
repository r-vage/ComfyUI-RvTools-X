# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, AnyType

any_type = AnyType("*")

class RvConversion_StringListToCombo:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "string": ("STRING", {"forceInput": True},
                    "Delimited string to split into combo items.\nNon-string input returns as-is."),
                "separator": ("STRING", {"default": "$"}, "Separator to use for splitting."),
            },
            "optional": {
                "index": ("INT", {"default": 0}, "Index of item to extract (0-based). Out-of-range returns last item."),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.CONVERSION.value
    RETURN_TYPES = (any_type,)
    FUNCTION = "execute"

    def execute(self, string, separator, index=0):
        # Type safety: handle None and non-string input
        if string is None or not isinstance(string, str):
            return (string,)
        if not separator or separator not in string:
            return (string,)
        splitted = string.split(separator)
        # Defensive: handle out-of-range index
        if not isinstance(index, int) or index < 0:
            index = 0
        if index >= len(splitted):
            return (splitted[-1],)
        return (splitted[index],)

NODE_NAME = "Stringlist to Combo [RvTools-X]"
NODE_DESC = "Stringlist to Combo"

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvConversion_StringListToCombo
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
