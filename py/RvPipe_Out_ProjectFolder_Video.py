# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import torch
import comfy.model_management
from ..core import CATEGORY

class RvPipe_Out_ProjectFolder_Video:
    def __init__(self):
        self.device = comfy.model_management.intermediate_device()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pipe": ("pipe", {"tooltip": "Input dict-style pipe containing width, height, batch size, frame rate, frame load cap, skip frames, select nth, and path."}),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PIPE.value
    RETURN_TYPES = ("INT",   "INT",    "FLOAT",      "INT",            "INT",               "INT",              "LATENT", "STRING")
    RETURN_NAMES = ("width", "height", "frame_rate", "frame_load_cap", "skip_first_frames", "select_every_nth", "latent", "path")
    FUNCTION = "execute"
    
    def execute(self, pipe: dict = None) -> tuple:
        # Only accept dict-style pipes now.
        if pipe is None:
            raise ValueError("Input pipe must not be None and must be a dict-style pipe")
        if not isinstance(pipe, dict):
            raise ValueError("RvPipe_Out_ProjectFolder_Video expects dict-style pipes only.")

        try:
            width = int(pipe.get("width")) if pipe.get("width") is not None else 0
        except Exception:
            width = 0
        try:
            height = int(pipe.get("height")) if pipe.get("height") is not None else 0
        except Exception:
            height = 0
        try:
            frame_rate = float(pipe.get("frame_rate")) if pipe.get("frame_rate") is not None else 30.0
        except Exception:
            frame_rate = 30.0
        try:
            frame_load_cap = int(pipe.get("frame_load_cap")) if pipe.get("frame_load_cap") is not None else 0
        except Exception:
            frame_load_cap = 0
        try:
            skip_first_frames = int(pipe.get("skip_first_frames")) if pipe.get("skip_first_frames") is not None else 0
        except Exception:
            skip_first_frames = 0
        try:
            select_every_nth = int(pipe.get("select_every_nth")) if pipe.get("select_every_nth") is not None else 1
        except Exception:
            select_every_nth = 1
        try:
            batch_size = int(pipe.get("batch_size")) if pipe.get("batch_size") is not None else 1
        except Exception:
            batch_size = 1

        path = pipe.get("path") or ""

        # Generate latent with the given width and height
        output_latent = self.generate(width, height, batch_size)[0]

        return (width, height, frame_rate, frame_load_cap, skip_first_frames, select_every_nth, output_latent, path)

    def generate(self, width, height, batch_size=1):
        latent = torch.zeros([batch_size, 4, height // 8, width // 8], device=self.device)
        return ({"samples":latent},)
                

NODE_NAME = 'Pipe Out Project Folder Video [RvTools-X]'
NODE_DESC = 'Pipe Out Project Folder Video'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvPipe_Out_ProjectFolder_Video
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}