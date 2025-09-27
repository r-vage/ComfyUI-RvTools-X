# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY

class RvConversion_LoraStackToString:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "lora_stack": ("LORA_STACK", {},
                    "List of LoRA tuples (STR, FLOAT1, FLOAT2).\nReturns a space-separated string in <lora:...> format."),
                "remove_weight": ("BOOLEAN", {"default": False}, "If true, removes the last 2 elements from each tuple, using only the LoRA name.")
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("LoRA string",)
    FUNCTION = "convert"
    CATEGORY = CATEGORY.MAIN.value + CATEGORY.CONVERSION.value

    def convert(self, lora_stack, remove_weight):
        # Type safety: handle None and non-iterable input
        if lora_stack is None or not hasattr(lora_stack, "__iter__"):
            return ("",)
        try:
            if remove_weight:
                output = ' '.join(
                    f"<lora:{str(tup[0])}>"
                    for tup in lora_stack
                    if isinstance(tup, (list, tuple)) and len(tup) >= 1
                )
            else:
                output = ' '.join(
                    f"<lora:{str(tup[0])}:{str(tup[1])}:{str(tup[2])}>"
                    for tup in lora_stack
                    if isinstance(tup, (list, tuple)) and len(tup) >= 3
                )
            return (output,)
        except Exception:
            return ("",)

NODE_NAME = "Lora Stack to String [RvTools-X]"
NODE_DESC = "Lora Stack to String"

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvConversion_LoraStackToString
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}

