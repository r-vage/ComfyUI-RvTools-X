# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import os
import folder_paths
import json
from datetime import datetime
from ..core import CATEGORY, cstr
from ..core import AnyType

batchnum = int(0)
skipnum = int(0)
any = AnyType("*")

MAX_RESOLUTION = 32768

def format_datetime(datetime_format):
    today = datetime.now()
    try:
        timestamp = today.strftime(datetime_format)
    except Exception:
        timestamp = today.strftime("%Y-%m-%d-%H%M%S")
    return timestamp

def format_date_time(string, position, datetime_format):
    today = datetime.now()
    if position == "prefix":
        return f"{today.strftime(datetime_format)}_{string}"
    if position == "postfix":
        return f"{string}_{today.strftime(datetime_format)}"
    return string

def format_variables(string, input_variables):
    if input_variables is not None and str(input_variables).strip():
        variables = str(input_variables).split(",")
        return string.format(*variables)
    else:
        return string

class RvFolders_ProjectFolder_Video:
    
    resolution =     ["Custom",
                      "480x832",
                      "576x1024",
                      "--- 9:16 ---",
                      "240x426 (240p)",              
                      "360x640 (360p)",
                      "480x853 (SD)",
                      "720x1280 (HD)",
                      "1080x1920 (FullHD)",
                      "1440x2560 (2K)",
                      "2160x3840 (4K)",
                      "4320x7680 (8K)",
                      "--- 16:9 ---",
                      "832x480",
                      "1024x576",
                      "426x240 (240p)",              
                      "640x360 (360p)",
                      "853x480 (SD)",
                      "1280x720x (HD)",
                      "1920x1080 (FullHD)",
                      "2560x1440 (2K)",
                      "3840x2160 (4K)",
                      "7680x4320 (8K)",                      
                      ]

    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "project_root_name": ("STRING", {"multiline": False, "default": "vGEN", "tooltip": "Root folder name for the video project."}),
                "date_time_format": ("STRING", {"multiline": False, "default": "%Y-%m-%d", "tooltip": "Format for date/time (strftime)."}),
                "add_date_time": (["disable", "prefix", "postfix"], {"default": "postfix", "tooltip": "Add date/time as prefix or postfix to folder name."}),
                "batch_folder_name": ("STRING", {"multiline": False, "default": "batch_{}", "tooltip": "Batch subfolder name, use {} for batch number."}),                
                "create_batch_folder": ("BOOLEAN", {"default": True, "tooltip": "Create a batch subfolder inside the project folder."}),
                "resolution": (cls.resolution, {"tooltip": "Select video resolution preset or use custom width/height."}),
                "width": ("INT", {"default": 576, "min": 16, "max": MAX_RESOLUTION, "step": 1, "tooltip": "Video width in pixels (used if Custom or to override preset)."}),
                "height": ("INT", {"default": 1024, "min": 16, "max": MAX_RESOLUTION, "step": 1, "tooltip": "Video height in pixels (used if Custom or to override preset)."}),
                "frame_rate": ("FLOAT", {"default": 30.0, "min": 8, "max": 240, "tooltip": "Video frame rate (frames per second)."}),
                "frame_load_cap": ("INT", {"default": 81, "min": -1, "max": MAX_RESOLUTION, "step": 1, "tooltip": "Maximum frames to load per batch."}),
                "skip_first_frames": ("INT", {"default": 0, "min": 0, "max": 4096, "tooltip": "Number of initial frames to skip."}),
                "skip_first_frames_calc": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "control_after_generate": True, "tooltip": "Additional skip calculation: skip (frame_load_cap * value)."}), 
                "select_every_nth": ("INT", {"default": 1, "min": 1, "max": 100, "tooltip": "Select every nth frame from input."}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 100, "tooltip": "Batch size for latent generation."}),
                "batch_number": ("INT", {"default": 1, "min": 1, "max": 0xffffffffffffffff, "control_after_generate": True, "tooltip": "Batch number to use in batch folder name."}),                
            },
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.FOLDER.value
    RETURN_TYPES = ("pipe",)
    FUNCTION = "execute"
    
    def execute(self, project_root_name, add_date_time, date_time_format, create_batch_folder, batch_folder_name, frame_rate, frame_load_cap, skip_first_frames, select_every_nth, batch_size, resolution, width, height, batch_number, skip_first_frames_calc):
        # Type safety: ensure valid strings and numbers
        if not isinstance(project_root_name, str) or not project_root_name:
            project_root_name = "vGEN"
        if not isinstance(date_time_format, str) or not date_time_format:
            date_time_format = "%Y-%m-%d"
        if not isinstance(batch_folder_name, str) or not batch_folder_name:
            batch_folder_name = "batch_{}"
        if not isinstance(frame_rate, (int, float)):
            frame_rate = 30.0
        if not isinstance(frame_load_cap, int):
            frame_load_cap = 81
        if not isinstance(skip_first_frames, int):
            skip_first_frames = 0
        if not isinstance(select_every_nth, int):
            select_every_nth = 1
        if not isinstance(batch_size, int):
            batch_size = 1
        if not isinstance(batch_number, int):
            batch_number = 1
        if not isinstance(skip_first_frames_calc, int):
            skip_first_frames_calc = 0

        mDate = format_datetime(date_time_format)
        new_path = project_root_name
        batchnum = batch_number
        skipnum = skip_first_frames_calc

        if add_date_time == "prefix":
            new_path = os.path.join(mDate, project_root_name)
        elif add_date_time == "postfix":
            new_path = os.path.join(project_root_name, mDate)

        if create_batch_folder:
            folder_name_parsed = format_variables(batch_folder_name, batchnum)
            new_path = os.path.join(new_path, folder_name_parsed)

        if skipnum > 0:
            try:
                skip_first_frames = skip_first_frames + (frame_load_cap * skipnum)
            except Exception:
                skip_first_frames = 0

        # Resolution presets
        resolution_map = {
            "480x832": (480, 832),
            "576x1024": (576, 1024),
            "240x426 (240p)": (240, 426),
            "360x640 (360p)": (360, 640),
            "480x853 (SD)": (480, 853),
            "720x1280 (HD)": (720, 1280),
            "1080x1920 (FullHD)": (1080, 1920),
            "1440x2560 (2K)": (1440, 2560),
            "2160x3840 (4K)": (2160, 3840),
            "4320x7680 (8K)": (4320, 7680),
            "832x480": (832, 480),
            "1024x576": (1024, 576),
            "426x240 (240p)": (426, 240),
            "640x360 (360p)": (640, 360),
            "853x480 (SD)": (853, 480),
            "1280x720x (HD)": (1280, 720),
            "1920x1080 (FullHD)": (1920, 1080),
            "2560x1440 (2K)": (2560, 1440),
            "3840x2160 (4K)": (3840, 2160),
            "7680x4320 (8K)": (7680, 4320),
        }
        if resolution in resolution_map:
            width, height = resolution_map[resolution]

        # Build output path
        Path = os.path.join(self.output_dir, new_path)

        # Build a pipe dict compatible with RvPipe_In* nodes
        pipe = {
            "path": str(Path),
            "width": int(width),
            "height": int(height),
            "frame_rate": float(frame_rate),
            "frame_load_cap": int(frame_load_cap),
            "skip_first_frames": int(skip_first_frames),
            "select_every_nth": int(select_every_nth),
            "batch_size": int(batch_size),
        }

        return (pipe,)

NODE_NAME = 'Project Folder Video [RvTools-X]'
NODE_DESC = 'Project Folder Video'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvFolders_ProjectFolder_Video
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}