# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import comfy
from ..core import CATEGORY, purge_vram

SAMPLERS_COMFY = comfy.samplers.KSampler.SAMPLERS

class RvPasser_Sampler:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (SAMPLERS_COMFY, {"forceInput": True, "tooltip": "Sampler name to be passed through."}),
                "Purge_VRAM": ("BOOLEAN", {"default": False, "tooltip": "If enabled, purges VRAM and unloads all models before passing Sampler."}),
            },
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PASSER.value
    RETURN_TYPES = (SAMPLERS_COMFY,)
    RETURN_NAMES = ("sampler_name",)
    FUNCTION = "passthrough"

    def passthrough(self, input: str, Purge_VRAM: bool) -> tuple:
        # Returns the sampler_name input as output.

        if Purge_VRAM:
            purge_vram()

        return (input,)

NODE_NAME = 'Pass Sampler [RvTools-X]'
NODE_DESC = 'Pass Sampler'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvPasser_Sampler
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}