# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, purge_vram

class RvPasser_VAE:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("VAE", {"tooltip": "VAE input to be passed through."}),
                "Purge_VRAM": ("BOOLEAN", {"default": False, "tooltip": "If enabled, purges VRAM and unloads all models before passing VAE."}),
            },
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PASSER.value
    RETURN_TYPES = ("VAE",)
    RETURN_NAMES = ("vae",)
    FUNCTION = "passthrough"

    def passthrough(self, input: object, Purge_VRAM: bool) -> tuple:
        # Returns the VAE input as output.

        if Purge_VRAM:
            purge_vram()

        return (input,)

NODE_NAME = 'Pass Vae [RvTools-X]'
NODE_DESC = 'Pass Vae'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvPasser_VAE
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}