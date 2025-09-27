# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY
import re

class RvConversion_MergeStrings:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "string_1": ("STRING", {"forceInput": True, "default": "", "tooltip": "First string to merge."}),
                "string_2": ("STRING", {"forceInput": True, "default": "", "tooltip": "Second string to merge."}),
                "string_3": ("STRING", {"forceInput": True, "default": "", "tooltip": "Third string to merge."}),
                "string_4": ("STRING", {"forceInput": True, "default": "", "tooltip": "Fourth string to merge."}),
                "string_5": ("STRING", {"forceInput": True, "default": "", "tooltip": "Fifth string to merge."}),
                "Delimiter": ("STRING", {"default": ", ", "tooltip": "Delimiter to use between strings (e.g. ', ', '\\n')."}),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.CONVERSION.value
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    FUNCTION = "execute"

    def execute(self, Delimiter: str = ", ", **kwargs) -> tuple[str]:
        # Merge input strings using the specified delimiter, replacing line breaks in output with spaces.
        text_inputs: list[str] = []

        # Normalize delimiter for literal newlines
        if Delimiter in ("\n", "\\n"):
            Delimiter = "\n"

        # Collect non-empty string inputs in sorted order
        for k in sorted(kwargs.keys()):
            v = kwargs[k]
            if isinstance(v, str) and v:
                text_inputs.append(v)

        merged_text = Delimiter.join(text_inputs)
        # Replace all line breaks with spaces for prompt output
        merged_text = re.sub(r"[\r\n]+", " ", merged_text)

        return (merged_text,)

NODE_NAME = 'Merge Strings [RvTools-X]'
NODE_DESC = 'Merge Strings'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvConversion_MergeStrings
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}