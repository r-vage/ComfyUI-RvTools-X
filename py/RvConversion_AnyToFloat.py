# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, AnyType
from collections.abc import Iterable

any_type = AnyType("*")

class RvConversion_AnyToFloat:
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
    RETURN_TYPES = ("FLOAT",)

    FUNCTION = "execute"

    def execute(self, input: object) -> tuple:
        # Converts any input value to a float, handling common types robustly.
        # Returns 0.0 for None or unconvertible types. Handles bytes, lists, dicts, sets, and iterables safely.
        if input is None:
            return (0.0,)
        # Direct float
        if isinstance(input, float):
            return (input,)
        # Integer
        if isinstance(input, int):
            return (float(input),)
        # String
        if isinstance(input, str):
            try:
                return (float(input.strip()),)
            except Exception:
                return (0.0,)
        # Bytes
        if isinstance(input, (bytes, bytearray)):
            try:
                s = input.decode("utf-8", errors="replace").strip()
                return (float(s),)
            except Exception:
                return (0.0,)
        # Iterable (list, tuple, numpy, etc)
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
            if seq is not None and len(seq) > 0:
                # Try to convert first element
                try:
                    return (float(seq[0]),)
                except Exception:
                    return (0.0,)
            return (0.0,)
        # Dict, set: not convertible
        if isinstance(input, (dict, set)):
            return (0.0,)
        # Fallback: try to convert
        try:
            return (float(str(input).strip()),)
        except Exception:
            return (0.0,)

NODE_NAME = "Any to Float [RvTools-X]"
NODE_DESC = "Any to Float"

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvConversion_AnyToFloat
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}