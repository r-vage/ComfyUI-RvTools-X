# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, purge_vram

class RvPasser_Float:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("FLOAT", {"forceInput": True, "tooltip": "Float input to be passed through."}),
                "Purge_VRAM": ("BOOLEAN", {"default": False, "tooltip": "If enabled, purges VRAM and unloads all models before passing Float."}),
            },
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PASSER.value
    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "passthrough"

    def passthrough(self, input: float, Purge_VRAM: bool) -> tuple:
        # Returns the float input as output.

        if Purge_VRAM:
            purge_vram()

        return (input,)

NODE_NAME = 'Pass Float [RvTools-X]'
NODE_DESC = 'Pass Float'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvPasser_Float
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}