# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from __future__ import annotations
from ..core import CATEGORY, purge_vram

class RvSwitch_Multi_Latent:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "inputcount": ("INT", {"default": 2, "min": 1, "max": 64, "step": 1, "tooltip": "Number of latent inputs to expose; click 'Update inputs' to add or remove inputs."}),
                "Purge_VRAM": ("BOOLEAN", {"default": False, "tooltip": "If enabled, purges VRAM before switching."}),
            },
            "optional": {
                "latent_1": ("LATENT", {"tooltip": "Latent input #1 (highest priority). Leave empty to bypass."}),
                "latent_2": ("LATENT", {"tooltip": "Latent input #2 (used if #1 is empty)."}),
            }
        }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    FUNCTION = "select"
    CATEGORY = CATEGORY.MAIN.value +  CATEGORY.MULTISWITCHES.value
    DESCRIPTION = "Multi-switch for LATENT inputs. Click 'Update inputs' (frontend) to add/remove latent_X inputs."

    def select(self, inputcount, Purge_VRAM=False, **kwargs):
        if Purge_VRAM:
            purge_vram()

        def _is_empty(v):
            if v is None:
                return True
            return False

        for i in range(1, max(1, inputcount) + 1):
            key = f"latent_{i}"
            val = kwargs.get(key)
            if not _is_empty(val):
                return (val,)

        raise RuntimeError(f"RvSwitch_Multi_Latent: no latent found among latent_1..latent_{inputcount}.")

NODE_NAME = 'Latent Multi-Switch [RvTools-X]'
NODE_DESC = 'Latent Multi-Switch'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvSwitch_Multi_Latent
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
