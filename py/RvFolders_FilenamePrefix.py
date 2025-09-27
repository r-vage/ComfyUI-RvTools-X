# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import os
from datetime import datetime
from ..core import CATEGORY, AnyType

any = AnyType("*")

def format_datetime(datetime_format):
    today = datetime.now()
    try:
        timestamp = today.strftime(datetime_format)
    except:
        timestamp = today.strftime("%Y-%m-%d-%H%M%S")

    return timestamp

def format_date_time(string, position, datetime_format):
    today = datetime.now()
    if position == "prefix":
        return f"{today.strftime(datetime_format)}_{string}"
    if position == "postfix":
        return f"{string}_{today.strftime(datetime_format)}"

def format_variables(string, input_variables):
    if input_variables:
        variables = str(input_variables).split(",")
        return string.format(*variables)
    else:
        return string

class RvFolders_FilenamePrefix:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_name_prefix": ("STRING", {"multiline": False, "default": "image"}, "Filename prefix to join to the base path. Type-safe: handles None and empty input."),
                "add_date_time": (["disable", "prefix", "postfix"], {}, "Add date/time to the filename prefix. Options: disable, prefix, postfix."),
                "date_time_format": ("STRING", {"multiline": False, "default": "%Y-%m-%d_%H:%M:%S"}, "Date/time format for prefix/postfix."),
            },
            "optional": {
                "path_opt": ("STRING", {"forceInput": True}, "Optional base path to which the filename prefix will be added. If not provided, only the prefix is created."),
                "input_variables": (any, {}, "Optional variables to format into the filename prefix.")
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.FOLDER.value
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)

    FUNCTION = "execute"

    def execute(self, file_name_prefix, add_date_time, date_time_format, path_opt=None, input_variables=None):
        # Joins a filename prefix (with optional date/time) to a base path, returning the new path as a string.
        # If no path is provided, returns only the prefix (with date/time if selected).
        # Handles None and empty input robustly.
        
        if not isinstance(file_name_prefix, str) or not file_name_prefix:
            file_name_prefix = "image"
        filename_name_parsed = format_variables(file_name_prefix, input_variables)
        if add_date_time == "disable":
            prefix = filename_name_parsed
        else:
            prefix = format_date_time(filename_name_parsed, add_date_time, date_time_format)
        if path_opt and isinstance(path_opt, str) and path_opt:
            new_path = os.path.join(path_opt, prefix)
        else:
            new_path = prefix
        return (new_path,)

NODE_NAME = 'Add Filename Prefix [RvTools-X]'
NODE_DESC = 'Add Filename Prefix'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvFolders_FilenamePrefix
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}