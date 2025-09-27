# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, AnyType

any_type = AnyType("*")

class RvConversion_AnyToString:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input": (any_type, {"default": "", "forceInput": True},
                    "Any value to convert to a string")
            },
            "optional": {
                "Delimiter": ("STRING", {"default": " ", "tooltip": "Delimiter used to join list/dict elements. Default is space."}),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.CONVERSION.value
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    
    INPUT_IS_LIST = (True, False)
    OUTPUT_IS_LIST = (False,)

    FUNCTION = "execute"

    def execute(self, input, Delimiter: str = " "):
        # Ensure Delimiter is always a string, even if passed as a list
        if isinstance(Delimiter, list):
            if Delimiter:
                Delimiter = str(Delimiter[0])
            else:
                Delimiter = " "
        def flatten(val):
            result = []
            if isinstance(val, dict):
                for k, v in val.items():
                    if isinstance(v, (list, tuple, dict)):
                        for item in flatten(v):
                            result.append(f"{k}: {item}")
                    elif isinstance(v, str) and '\n' in v:
                        for line in v.splitlines():
                            result.append(f"{k}: {line}")
                    else:
                        result.append(f"{k}: {v}")
            elif isinstance(val, (list, tuple)):
                for el in val:
                    if isinstance(el, (list, tuple, dict)):
                        result.extend(flatten(el))
                    elif isinstance(el, str) and '\n' in el:
                        result.extend(el.splitlines())
                    else:
                        result.append(str(el))
            elif isinstance(val, str) and '\n' in val:
                result.extend(val.splitlines())
            else:
                result.append(str(val))
            return result

        # If input is a list from the node system, flatten each item and join all
        if isinstance(input, list):
            flat = []
            for item in input:
                flat.extend(flatten(item))
            return (str(Delimiter).join(flat),)
        elif isinstance(input, (tuple, dict)):
            return (str(Delimiter).join(flatten(input)),)
        return (str(input),)


NODE_NAME = "Any to String [RvTools-X]"
NODE_DESC = "Any to String"

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvConversion_AnyToString
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}