# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, AnyType
from collections.abc import Iterable

any_type = AnyType("*")

class RvConversion_AnyToCombo:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input": (any_type, {"default": "", "forceInput": True},
                    "Any value to convert to a string.\nHandles None, bytes, lists, dicts, etc.\nLists of strings are auto-joined with ', '.")
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.CONVERSION.value
    RETURN_TYPES = ("COMBO",)

    FUNCTION = "execute"

    def _scalar_to_str(self, value):
        """Convert a scalar value to a safe string for combo use."""
        if value is None:
            return ""
        if isinstance(value, str):
            return value
        if isinstance(value, (bytes, bytearray)):
            try:
                return value.decode("utf-8", errors="replace")
            except Exception:
                return str(value)
        try:
            return f"{value}"
        except Exception:
            return repr(value)

    def execute(self, input):
        # Return a COMBO-compatible tuple: (selected_value, options_list).
        #
        # - For iterable inputs (not string/bytes), options_list will be the stringified
        #   elements; selected_value is the first element string (or empty string for empty).
        # - For scalars, options_list is a single-item list containing the converted string,
        #   and selected_value is that string.

        if isinstance(input, Iterable) and not isinstance(input, (str, bytes, bytearray)):
            seq = None
            if hasattr(input, "tolist") and not isinstance(input, (list, tuple)):
                try:
                    seq = input.tolist()
                except Exception:
                    seq = None
            else:
                try:
                    seq = list(input)
                except Exception:
                    seq = None

            if seq is None:
                # Fallback to stringifying the input itself as single option
                s = self._scalar_to_str(input)
                return (s, [s])

            # Stringify each element safely
            try:
                options = [self._scalar_to_str(x) for x in seq]
            except Exception:
                # If something goes wrong, fallback to the stringified whole
                s = self._scalar_to_str(input)
                return (s, [s])

            if len(options) == 0:
                return ("", [])
            return (options[0], options)

        # Non-iterable scalars
        s = self._scalar_to_str(input)
        return (s, [s])

NODE_NAME = "Any to Combo [RvTools-X]"
NODE_DESC = "Any to Combo"

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvConversion_AnyToCombo
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}