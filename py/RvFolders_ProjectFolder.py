# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import os
import folder_paths

from datetime import datetime
from ..core import CATEGORY, AnyType
from ..core.common import RESOLUTION_PRESETS, RESOLUTION_MAP

any = AnyType("*")

MAX_RESOLUTION = 32768

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

class RvFolders_ProjectFolder:
    resolution = RESOLUTION_PRESETS
    resolution_map = RESOLUTION_MAP

    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "project_root_name": ("STRING", {"multiline": False, "default": "MyProject"}, "Project root folder name."),
                "date_time_format": ("STRING", {"multiline": False, "default": "%Y-%m-%d"}, "Date/time format for folder naming (strftime syntax)."),
                "add_date_time": (["disable", "prefix", "postfix"], {"default": "postfix"}, "Where to add date/time to folder name: disable, prefix, or postfix."),
                "batch_folder_name": ("STRING", {"multiline": False, "default": "batch_{}"}, "Batch subfolder name. Supports variable formatting (e.g. batch_{})."),
                "create_batch_folder": ("BOOLEAN", {"default": False}, "Create a batch subfolder if enabled."),
                "resolution": (cls.resolution, {}, "Image resolution preset."),
                "width": ("INT", {"default": 512, "min": 16, "max": MAX_RESOLUTION, "step": 8}, "Image width in pixels."),
                "height": ("INT", {"default": 512, "min": 16, "max": MAX_RESOLUTION, "step": 8}, "Image height in pixels."),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 4096}, "Batch size (number of images per batch)."),
                "batch_number": ("INT", {"default": 1, "min": 1, "max": 0xffffffffffffffff, "control_after_generate": True, "tooltip": "Batch number to use in batch folder name."}),                                
            },
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.FOLDER.value
    # Add a 'pipe' output (a dict) as first return so this node can be connected
    # directly to RvPipe_In* nodes which accept a pipe/context dict.
    RETURN_TYPES = ("pipe",)
    RETURN_NAMES = ("pipe",)

    FUNCTION = "execute"

    def execute(self, project_root_name, add_date_time, date_time_format, create_batch_folder, batch_folder_name, batch_size, resolution, width, height, batch_number):
        if not isinstance(project_root_name, str) or not project_root_name:
            project_root_name = "MyProject"
        if not isinstance(date_time_format, str) or not date_time_format:
            date_time_format = "%Y-%m-%d"
        mDate = format_datetime(date_time_format)
        new_path = project_root_name

        if add_date_time == "prefix":
            new_path = os.path.join(mDate, project_root_name)
        elif add_date_time == "postfix":
            new_path = os.path.join(project_root_name, mDate)

        if create_batch_folder:
            folder_name_parsed = format_variables(batch_folder_name, batch_number)
            new_path = os.path.join(new_path, folder_name_parsed)

        if resolution in self.resolution_map:
            width, height = self.resolution_map[resolution]

        # Build a pipe/context dict compatible with RvPipe_In* nodes.
        path_out = os.path.join(self.output_dir, new_path)

        pipe = {
            "path": path_out,
            "width": width,
            "height": height,
            "batch_size": batch_size,
        }

        # Return the pipe first, then the individual values (path, width, height, batch_size)
        return (pipe, path_out, width, height, batch_size)


NODE_NAME = 'Project Folder [RvTools-X]'
NODE_DESC = 'Project Folder'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvFolders_ProjectFolder
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
