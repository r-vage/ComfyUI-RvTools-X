# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, purge_vram

class RvPasser_Supir_Vae:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("SUPIRVAE", {"tooltip": "SUPIRVAE input to be passed through."}),
                "Purge_VRAM": ("BOOLEAN", {"default": False, "tooltip": "If enabled, purges VRAM and unloads all models before passing SUPIRVAE."}),
            },
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PASSER.value
    RETURN_TYPES = ("SUPIRVAE",)
    RETURN_NAMES = ("SUPIR_VAE",)
    FUNCTION = "passthrough"

    def passthrough(self, input: object, Purge_VRAM: bool) -> tuple:
        # Returns the SUPIRVAE input as output.

        if Purge_VRAM:
            purge_vram()

        return (input,)

NODE_NAME = 'Pass SUPIR_VAE [RvTools-X]'
NODE_DESC = 'Pass SUPIR_VAE'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvPasser_Supir_Vae
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
