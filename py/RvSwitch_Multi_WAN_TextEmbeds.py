# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, purge_vram, cstr

class RvSwitch_Multi_WAN_TextEmbeds:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Purge_VRAM": ("BOOLEAN", {"default": False, "tooltip": "If enabled, purges VRAM and unloads all models before switching."}),
            },
            "optional": {
                "input1": ("WANVIDEOTEXTEMBEDS", {"forceInput": True, "tooltip": "First input (highest priority)."}),
                "input2": ("WANVIDEOTEXTEMBEDS", {"forceInput": True, "tooltip": "Second input (used if input1 is None)."}),
                "input3": ("WANVIDEOTEXTEMBEDS", {"forceInput": True, "tooltip": "Third input (used if input1 and input2 are None)."}),
                "input4": ("WANVIDEOTEXTEMBEDS", {"forceInput": True, "tooltip": "Fourth input (used if previous are None)."}),
                "input5": ("WANVIDEOTEXTEMBEDS", {"forceInput": True, "tooltip": "Fifth input (used if previous are None)."}),
            }
        }


    CATEGORY = CATEGORY.MAIN.value + CATEGORY.MULTISWITCHES.value
    RETURN_TYPES = ("WANVIDEOTEXTEMBEDS",)
    RETURN_NAMES = ("text_embeds",)
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
        # Returns the first non-None WANVIDEOTEXTEMBEDS input. Optionally purges VRAM.
        if Purge_VRAM:
            purge_vram()

        for text_embeds in (input1, input2, input3, input4, input5):
            if text_embeds is not None:
                return (text_embeds,)
        raise ValueError("Missing Input: Multi Text_Embeds Switch has no active Input")

NODE_NAME = 'WAN Text_Embeds Multi-Switch [RvTools-X]'
NODE_DESC = 'WAN Text_Embeds Multi-Switch'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvSwitch_Multi_WAN_TextEmbeds
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}