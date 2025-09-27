# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, purge_vram

class RvSwitch_Multi_WAN_VAE:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Purge_VRAM": ("BOOLEAN", {"default": False, "tooltip": "If enabled, purges VRAM and unloads all models before switching."}),
            },
            "optional": {
                "input1": ("WANVAE", {"forceInput": True, "tooltip": "First input (highest priority)."}),
                "input2": ("WANVAE", {"forceInput": True, "tooltip": "Second input (used if input1 is None)."}),
                "input3": ("WANVAE", {"forceInput": True, "tooltip": "Third input (used if input1 and input2 are None)."}),
                "input4": ("WANVAE", {"forceInput": True, "tooltip": "Fourth input (used if previous are None)."}),
                "input5": ("WANVAE", {"forceInput": True, "tooltip": "Fifth input (used if previous are None)."}),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.MULTISWITCHES.value
    RETURN_TYPES = ("WANVAE",)
    RETURN_NAMES = ("vae",)

    FUNCTION = "execute"

    def execute(self, Purge_VRAM, input1=None, input2=None, input3=None, input4=None, input5=None):
        if Purge_VRAM:
            purge_vram()

        for vae in (input1, input2, input3, input4, input5):
            if vae is not None:
                return (vae,)
        
        raise ValueError("Missing Input: Multi VAE Switch has no active Input")

NODE_NAME = 'WAN_VAE Multi-Switch [RvTools-X]'
NODE_DESC = 'WAN_VAE Multi-Switch'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvSwitch_Multi_WAN_VAE
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}