# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, purge_vram

class RvSwitch_Multi_Float:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Purge_VRAM": ("BOOLEAN", {"default": False, "tooltip": "If enabled, purges VRAM and unloads all models before switching."}),
            },
            "optional": {
                "input1": ("FLOAT", {"forceInput": True, "tooltip": "First input (highest priority)."}),
                "input2": ("FLOAT", {"forceInput": True, "tooltip": "Second input (used if input1 is None)."}),
                "input3": ("FLOAT", {"forceInput": True, "tooltip": "Third input (used if input1 and input2 are None)."}),
                "input4": ("FLOAT", {"forceInput": True, "tooltip": "Fourth input (used if previous are None)."}),
                "input5": ("FLOAT", {"forceInput": True, "tooltip": "Fifth input (used if previous are None)."}),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.MULTISWITCHES.value
    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("float",)

    FUNCTION = "execute"

    def execute(self, Purge_VRAM=False, input1=None, input2=None, input3=None, input4=None, input5=None):
        # Passes through the first non-None FLOAT input from up to five inputs.
        # Handles None and empty input robustly.
        #
        if Purge_VRAM:
            purge_vram()
                    
        for inp in (input1, input2, input3, input4, input5):
            if inp is not None:
                return (inp,)
        raise ValueError("Missing Input: Multi Float Switch has no active Input")

NODE_NAME = 'Float Multi-Switch [RvTools-X]'
NODE_DESC = 'Float Multi-Switch'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvSwitch_Multi_Float
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}