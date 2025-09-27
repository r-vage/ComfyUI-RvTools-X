# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY

MAX_RESOLUTION = 32768

class RvSettings_CustomSize:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 16, "max": MAX_RESOLUTION, "step": 8, "tooltip": "Set the custom width (16-32768, step 8)."}),
                "height": ("INT", {"default": 512, "min": 16, "max": MAX_RESOLUTION, "step": 8, "tooltip": "Set the custom height (16-32768, step 8)."}),
            },
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.SETTINGS.value
    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "execute"

    def execute(self, width: int, height: int) -> tuple:
        # Returns the validated custom width and height for workflow use.
        return (width, height)

NODE_NAME = 'Custom Size [RvTools-X]'
NODE_DESC = 'Custom Size'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvSettings_CustomSize
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}