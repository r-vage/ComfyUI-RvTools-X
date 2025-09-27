# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, purge_vram

class RvPasser_Controlnet:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("CONTROL_NET", {"tooltip": "ControlNet input to be passed through."}),
                "Purge_VRAM": ("BOOLEAN", {"default": False, "tooltip": "If enabled, purges VRAM and unloads all models before passing ControlNet."}),
            },
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PASSER.value
    RETURN_TYPES = ("CONTROL_NET",)
    FUNCTION = "passthrough"

    def passthrough(self, input: object, Purge_VRAM: bool) -> tuple:
        # Returns the ControlNet input as output.

        if Purge_VRAM:
            purge_vram()

        return (input,)

NODE_NAME = 'Pass ControlNet [RvTools-X]'
NODE_DESC = 'Pass ControlNet'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvPasser_Controlnet
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}