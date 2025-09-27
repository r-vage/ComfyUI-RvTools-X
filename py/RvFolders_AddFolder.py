# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import os
from ..core import CATEGORY

class RvFolders_AddFolder:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"forceInput": True}, "Base path to which the folder will be added.\nType-safe: handles None and empty input."),
                "folder_name": ("STRING", {"multiline": False, "default": "SubFolder"}, "Folder name to join to the base path.\nType-safe: handles None and empty input."),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.FOLDER.value
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)    
    
    FUNCTION = "execute"

    def execute(self, path, folder_name):
        # Joins a folder name to a base path, returning the new path as a string.
        # Handles None and empty input robustly.

        if not isinstance(path, str) or not path:
            return ("",)
        if not isinstance(folder_name, str) or not folder_name:
            return (path,)
        new_path = os.path.join(path, folder_name)
        return (new_path,)

NODE_NAME = 'Add Folder [RvTools-X]'
NODE_DESC = 'Add Folder'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvFolders_AddFolder
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}