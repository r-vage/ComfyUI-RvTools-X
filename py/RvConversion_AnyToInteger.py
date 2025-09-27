# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, AnyType
from collections.abc import Iterable

any_type = AnyType("*")

class RvConversion_AnyToInteger:
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
    RETURN_TYPES = ("INT",)

    FUNCTION = "execute"

    def execute(self, input: object) -> tuple:
        # Converts any input value to an integer, handling common types robustly.
        # Returns 0 for None or unconvertible types. Handles bytes, lists, dicts, sets, and iterables safely.
        if input is None:
            return (0,)
        # Direct integer
        if isinstance(input, int):
            return (input,)
        # Float
        if isinstance(input, float):
            return (int(input),)
        # String
        if isinstance(input, str):
            try:
                return (int(float(input.strip())),)
            except Exception:
                return (0,)
        # Bytes
        if isinstance(input, (bytes, bytearray)):
            try:
                s = input.decode("utf-8", errors="replace").strip()
                return (int(float(s)),)
            except Exception:
                return (0,)
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
                    return (int(float(seq[0])),)
                except Exception:
                    return (0,)
            return (0,)
        # Dict, set: not convertible
        if isinstance(input, (dict, set)):
            return (0,)
        # Fallback: try to convert
        try:
            return (int(float(str(input).strip())),)
        except Exception:
            return (0,)

NODE_NAME = "Any to Integer [RvTools-X]"
NODE_DESC = "Any to Integer"

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvConversion_AnyToInteger
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}