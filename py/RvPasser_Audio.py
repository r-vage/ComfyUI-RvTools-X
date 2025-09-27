# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, purge_vram

class RvPasser_Audio:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("AUDIO", {"tooltip": "Audio input to be passed through."}),
                "Purge_VRAM": ("BOOLEAN", {"default": False, "tooltip": "If enabled, purges VRAM and unloads all models before passing Audio."}),
            },
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PASSER.value
    RETURN_TYPES = ("AUDIO",)
    FUNCTION = "passthrough"

    def passthrough(self, input: object, Purge_VRAM: bool) -> tuple:
        if Purge_VRAM:
            purge_vram()

        return (input,)

NODE_NAME = 'Pass Audio [RvTools-X]'
NODE_DESC = 'Pass Audio'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvPasser_Audio
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}