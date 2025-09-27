# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import sys
from ..core import CATEGORY

MAX_RESOLUTION = 32768

class RvVideo_WAN_Frames:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("INT", {"default": 81, "min": 1, "max": MAX_RESOLUTION, "step": 4, "tooltip": "Number of frames for WAN video workflows."}),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.VIDEO.value
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("int",)

    FUNCTION = "execute"

    def execute(self, value):
        # Outputs the number of frames for WAN video workflows.
        # Handles None and empty input robustly.
        if not isinstance(value, int):
            value = 81
        return (int(value),)

NODE_NAME = 'WAN_Frames [RvTools-X]'
NODE_DESC = 'WAN_Frames'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvVideo_WAN_Frames
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}