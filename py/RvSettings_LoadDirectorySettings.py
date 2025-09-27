# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY
from typing import List, Dict, Any, Tuple

class RvSettings_LoadDirectorySettings:
    CATEGORY = CATEGORY.MAIN.value + CATEGORY.SETTINGS.value
    RETURN_TYPES = ("pipe",)
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        return {
            "required": {
                "Directory": ("STRING", {"default": "", "tooltip": "Directory path to load files from."}),
                "start_index": ("INT", {"default": 0, "min": 0, "control_after_generate": True, "tooltip": "Start index for loading files."}),
                "loadcap": ("INT", {"default": 20, "tooltip": "Maximum number of files to load."}),
            },
        }

    def execute(
        self,
        Directory: str,
        start_index: int,
        loadcap: int
    ) -> Tuple[List[Any]]:
        # Return directory settings as a dict-style pipe for downstream nodes.
        pipe = {
            "directory": str(Directory),
            "start_index": int(start_index),
            "load_cap": int(loadcap),
        }
        return (pipe,)

NODE_NAME = 'Load Directory Settings [RvTools-X]'
NODE_DESC = 'Load Directory Settings'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvSettings_LoadDirectorySettings
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}