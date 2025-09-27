# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, purge_vram, cstr

class RvPasser_Conditioning:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("CONDITIONING", {"tooltip": "Conditioning input to be passed through."}),
                "Purge_VRAM": ("BOOLEAN", {"default": False, "tooltip": "If enabled, purges VRAM and unloads all models before passing Conditioning."}),
            },
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PASSER.value
    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "passthrough"

    def passthrough(self, input: object, Purge_VRAM: bool) -> tuple:
        # Returns the conditioning input as output.

        if Purge_VRAM:
            purge_vram()
        
        return (input,)

NODE_NAME = 'Pass Conditioning [RvTools-X]'
NODE_DESC = 'Pass Conditioning'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvPasser_Conditioning
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}