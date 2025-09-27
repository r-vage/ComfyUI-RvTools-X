# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, purge_vram

class RvSwitch_Multi_WAN_CacheArgs:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Purge_VRAM": ("BOOLEAN", {"default": False, "tooltip": "If enabled, purges VRAM and unloads all models before switching."}),
            },
            "optional": {
                "input1": ("CACHEARGS", {"forceInput": True, "tooltip": "First input (highest priority)."}),
                "input2": ("CACHEARGS", {"forceInput": True, "tooltip": "Second input (used if input1 is None)."}),
                "input3": ("CACHEARGS", {"forceInput": True, "tooltip": "Third input (used if input1 and input2 are None)."}),
                "input4": ("CACHEARGS", {"forceInput": True, "tooltip": "Fourth input (used if previous are None)."}),
                "input5": ("CACHEARGS", {"forceInput": True, "tooltip": "Fifth input (used if previous are None)."}),
            }
        }


    CATEGORY = CATEGORY.MAIN.value + CATEGORY.MULTISWITCHES.value
    RETURN_TYPES = ("CACHEARGS",)
    RETURN_NAMES = ("cache_args",)
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
        # Returns the first non-None CACHEARGS input. Optionally purges VRAM.
        #
        if Purge_VRAM:
            purge_vram()

        for cache_args in (input1, input2, input3, input4, input5):
            if cache_args is not None:
                return (cache_args,)
        return (None,)

NODE_NAME = 'WAN Cache Args Multi-Switch [RvTools-X]'
NODE_DESC = 'WAN Cache Args Multi-Switch'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvSwitch_Multi_WAN_CacheArgs
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}