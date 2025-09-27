# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY
from ..core.common import RESOLUTION_PRESETS, RESOLUTION_MAP
from typing import List, Dict, Any, Tuple

class RvSettings_Resolution_All:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        return {
            "required": {
                "resolution": (RESOLUTION_PRESETS[1:], {
                    "tooltip": "Select the aspect ratio and resolution for your image."
                }),
            },
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.SETTINGS.value
    RETURN_TYPES = ("INT", "INT",)
    RETURN_NAMES = ("width", "height")
    FUNCTION = "execute"

    def execute(self, resolution: str) -> Tuple[int, int]:
        # Return width and height for the selected resolution string.

        width, height = RESOLUTION_MAP.get(resolution, (512, 512))
        return width, height

NODE_NAME = 'Image Resolutions [RvTools-X]'
NODE_DESC = 'Image Resolutions'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvSettings_Resolution_All
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}