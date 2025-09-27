# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY

class RvPipe_Out_VHS_InputSettings:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pipe": ("pipe", {"tooltip": "Input dict-style pipe containing load_cap, skip_first_frames, select_every_nth, overlap, images_in_preview, images_in_filter_previews, preview_crop_pos, preview_crop_interpol, frame_rate."}),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PIPE.value
    RETURN_TYPES = ("INT", "INT", "INT", "INT", "INT", "INT", ["center","top", "bottom", "left", "right"], ["lanczos", "nearest", "bilinear", "bicubic", "area", "nearest-exact"], "FLOAT")
    RETURN_NAMES = ("load_cap", "skip_first_frames", "select_every_nth", "overlap", "images_in_previews", "images_in_filter_previews", "preview_crop_pos", "preview_crop_interpol", "frame_rate")
    FUNCTION = "execute"

    def execute(self, pipe: dict = None) -> tuple:
        # Only accept dict-style pipes now.
        if pipe is None:
            raise ValueError("Input pipe must not be None and must be a dict-style pipe")
        if not isinstance(pipe, dict):
            raise ValueError("RvPipe_Out_VHS_InputSettings expects dict-style pipes only.")

        try:
            load_cap = int(pipe.get("frame_load_cap")) if pipe.get("frame_load_cap") is not None else 0
        except Exception:
            load_cap = 0
        try:
            skip_first_frames = int(pipe.get("skip_first_frames")) if pipe.get("skip_first_frames") is not None else 0
        except Exception:
            skip_first_frames = 0
        try:
            select_every_nth = int(pipe.get("select_every_nth")) if pipe.get("select_every_nth") is not None else 1
        except Exception:
            select_every_nth = 1
        try:
            overlap = int(pipe.get("overlap")) if pipe.get("overlap") is not None else 0
        except Exception:
            overlap = 0
        try:
            images_in_previews = int(pipe.get("images_in_previews")) if pipe.get("images_in_previews") is not None else 0
        except Exception:
            images_in_previews = 0
        try:
            images_in_filter_previews = int(pipe.get("images_in_filter_previews")) if pipe.get("images_in_filter_previews") is not None else 0
        except Exception:
            images_in_filter_previews = 0

        preview_crop_pos = pipe.get("preview_crop_pos") or "center"
        preview_crop_interpol = pipe.get("preview_crop_interpol") or "lanczos"

        try:
            frame_rate = float(pipe.get("frame_rate")) if pipe.get("frame_rate") is not None else 30.0
        except Exception:
            frame_rate = 30.0

        return (load_cap, skip_first_frames, select_every_nth, overlap, images_in_previews, images_in_filter_previews, preview_crop_pos, preview_crop_interpol, frame_rate)

NODE_NAME = 'Pipe Out VHS Input Settings [RvTools-X]'
NODE_DESC = 'Pipe Out VHS Input Settings'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvPipe_Out_VHS_InputSettings
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}