# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, purge_vram, cstr

class RvSwitch_Multi_WAN_Model:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Purge_VRAM": ("BOOLEAN", {"default": False, "tooltip": "If enabled, purges VRAM and unloads all models before switching."}),
            },
            "optional": {
                "input1": ("WANVIDEOMODEL", {"forceInput": True, "tooltip": "First input (highest priority)."}),
                "input2": ("WANVIDEOMODEL", {"forceInput": True, "tooltip": "Second input (used if input1 is None)."}),
                "input3": ("WANVIDEOMODEL", {"forceInput": True, "tooltip": "Third input (used if input1 and input2 are None)."}),
                "input4": ("WANVIDEOMODEL", {"forceInput": True, "tooltip": "Fourth input (used if previous are None)."}),
                "input5": ("WANVIDEOMODEL", {"forceInput": True, "tooltip": "Fifth input (used if previous are None)."}),
            }
        }


    CATEGORY = CATEGORY.MAIN.value + CATEGORY.MULTISWITCHES.value
    RETURN_TYPES = ("WANVIDEOMODEL",)
    RETURN_NAMES = ("model",)
    FUNCTION = "execute"

    def execute(
        self,
        Purge_VRAM: bool,
        input1: object = None,
        input2: object = None,
        input3: object = None,
        input4: object = None,
        input5: object = None
    ):
        # Returns the first non-None WANVIDEOMODEL input. Optionally purges VRAM.       
        if Purge_VRAM:
            purge_vram()

        for model in (input1, input2, input3, input4, input5):
            if model is not None:
                return (model,)
        raise ValueError("Missing Input: Multi Switch WAN_Model has no active Input")

NODE_NAME = 'WAN_Model Multi-Switch [RvTools-X]'
NODE_DESC = 'WAN_Model Multi-Switch'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvSwitch_Multi_WAN_Model
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}