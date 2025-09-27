# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY

class RvPipe_Out_LoadDirectorySettings:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pipe": ("pipe", {"tooltip": "Input dict-style pipe containing directory, start_index, and load_cap."}),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PIPE.value
    RETURN_TYPES = ("STRING", "INT", "INT")
    RETURN_NAMES = ("directory", "start_index", "load_cap")
    FUNCTION = "execute"

    def execute(self, pipe: dict = None) -> tuple:
        # Only accept dict-style pipes now.
        if pipe is None:
            raise ValueError("Input pipe must not be None and must be a dict-style pipe")
        if not isinstance(pipe, dict):
            raise ValueError("RvPipe_Out_LoadDirectorySettings expects dict-style pipes only.")

        directory = pipe.get("directory") or pipe.get("path") or ""
        try:
            start_index = int(pipe.get("start_index")) if pipe.get("start_index") is not None else 0
        except Exception:
            start_index = 0
        try:
            load_cap = int(pipe.get("load_cap")) if pipe.get("load_cap") is not None else 0
        except Exception:
            load_cap = 0

        return (directory, start_index, load_cap)

NODE_NAME = 'Pipe Out Load Directory Settings [RvTools-X]'
NODE_DESC = 'Pipe Out Load Directory Settings'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvPipe_Out_LoadDirectorySettings
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}