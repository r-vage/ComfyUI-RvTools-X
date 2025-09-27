# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, purge_vram

class RvPasser_String:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("STRING", {"forceInput": True, "default": "", "tooltip": "String input to be passed through."}),
                "Purge_VRAM": ("BOOLEAN", {"default": False, "tooltip": "If enabled, purges VRAM and unloads all models before passing String."}),
            },
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PASSER.value
    RETURN_TYPES = ("STRING",)
    FUNCTION = "passthrough"

    def passthrough(self, input: str, Purge_VRAM: bool) -> tuple:
        # Returns the string input as output.

        if Purge_VRAM:
            purge_vram()

        return (input,)

NODE_NAME = 'Pass String [RvTools-X]'
NODE_DESC = 'Pass String'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvPasser_String
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}