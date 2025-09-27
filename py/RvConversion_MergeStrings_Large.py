# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY
from typing import Any, Dict, Tuple

class RvConversion_MergeStrings_Large:
   
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        return {
            "required": {},
            "optional": {
                "string_1": ("STRING", {"forceInput": True, "default": "", "tooltip": "First string input."}),
                "string_2": ("STRING", {"forceInput": True, "default": "", "tooltip": "Second string input."}),
                "string_3": ("STRING", {"forceInput": True, "default": "", "tooltip": "Third string input."}),
                "string_4": ("STRING", {"forceInput": True, "default": "", "tooltip": "Fourth string input."}),
                "string_5": ("STRING", {"forceInput": True, "default": "", "tooltip": "Fifth string input."}),
                "string_6": ("STRING", {"forceInput": True, "default": "", "tooltip": "Sixth string input."}),
                "string_7": ("STRING", {"forceInput": True, "default": "", "tooltip": "Seventh string input."}),
                "string_8": ("STRING", {"forceInput": True, "default": "", "tooltip": "Eighth string input."}),
                "string_9": ("STRING", {"forceInput": True, "default": "", "tooltip": "Ninth string input."}),
                "string_10": ("STRING", {"forceInput": True, "default": "", "tooltip": "Tenth string input."}),
                "Delimiter": ("STRING", {"default": ", ", "tooltip": "Delimiter to use when merging strings. Use \\n for newline."}),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.CONVERSION.value
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    FUNCTION = "execute"

    def execute(
        self,
        Delimiter: str,
        **kwargs: Any
    ) -> Tuple[str]:
        text_inputs = []

        # Handle special case where delimiter is "\n" (literal newline).
        if Delimiter in ("\n", "\\n"):
            Delimiter = "\n"

        # Iterate over the received inputs in sorted order.
        for k in sorted(kwargs.keys()):
            v = kwargs[k]
            # Only process string input ports.
            if isinstance(v, str) and v != "":
                text_inputs.append(v)

        merged_text = Delimiter.join(text_inputs)
        return (merged_text,)

NODE_NAME = 'Merge Strings (Large) [RvTools-X]'
NODE_DESC = 'Merge Strings (Large)'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvConversion_MergeStrings_Large
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}