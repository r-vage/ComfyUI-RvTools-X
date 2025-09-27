# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY
from typing import Any, Dict, List, Tuple

class RvSettings_VHS_InputSettings:
    CATEGORY = CATEGORY.MAIN.value + CATEGORY.SETTINGS.value
    RETURN_TYPES = ("pipe",)
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        return {
            "required": {
                "load_cap": ("INT", {"default": 20, "min": 0, "tooltip": "Maximum number of frames to load."}),
                "skip_first_frames": ("INT", {"default": 0, "min": 0, "tooltip": "Number of initial frames to skip."}),
                "select_every_nth": ("INT", {"default": 1, "min": 1, "tooltip": "Select every nth frame."}),
                "overlap": ("INT", {"default": 0, "min": 0, "tooltip": "Number of overlapping frames."}),
                "images_in_previews": ("INT", {"default": 10, "min": 1, "tooltip": "Number of images in preview."}),
                "images_in_filter_previews": ("INT", {"default": 1, "min": 1, "tooltip": "Number of images in filter preview."}),
                "preview_crop_pos": (["center", "top", "bottom", "left", "right"], {"tooltip": "Crop position for preview images."}),
                "crop_interpolation": (["lanczos", "nearest", "bilinear", "bicubic", "area", "nearest-exact"], {"tooltip": "Interpolation method for cropping."}),
                "frame_rate": ("FLOAT", {"default": 30, "min": 1, "tooltip": "Frame rate for video preview."}),
            },
        }

    def execute(
        self,
        load_cap: int,
        skip_first_frames: int,
        select_every_nth: int,
        overlap: int,
        images_in_previews: int,
        images_in_filter_previews: int,
        preview_crop_pos: str,
        crop_interpolation: str,
        frame_rate: float
    ) -> Tuple:
        pipe = {
            "frame_load_cap": int(load_cap),
            "skip_first_frames": int(skip_first_frames),
            "select_every_nth": int(select_every_nth),
            "overlap": int(overlap),
            "images_in_previews": int(images_in_previews),
            "images_in_filter_previews": int(images_in_filter_previews),
            "preview_crop_pos": preview_crop_pos,
            "crop_interpolation": crop_interpolation,
            "frame_rate": float(frame_rate),
        }
        return (pipe,)

NODE_NAME = 'VHS Input Settings [RvTools-X]'
NODE_DESC = 'VHS Input Settings'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvSettings_VHS_InputSettings
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
