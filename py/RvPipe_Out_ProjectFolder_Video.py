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
    RETURN_TYPES = ("INT", "INT", "FLOAT", "INT", ["INT"], ["INT"], "INT", "INT", "LATENT", "STRING")
    RETURN_NAMES = ("width", "height", "frame_rate", "frame_load_cap", "context_length", "overlap", "skip_first_frames", "select_every_nth", "latent", "path")
    FUNCTION = "execute"
    
    def execute(self, pipe: dict = None) -> tuple:
        # Only accept dict-style pipes now.
        if pipe is None:
            raise ValueError("Input pipe must not be None and must be a dict-style pipe")
        if not isinstance(pipe, dict):
            raise ValueError("RvPipe_Out_ProjectFolder_Video expects dict-style pipes only.")

        # Extract values - return None for missing keys to maintain compatibility with both V1 and V2
        width = pipe.get("width")
        height = pipe.get("height") 
        frame_rate = pipe.get("frame_rate")
        frame_load_cap = pipe.get("frame_load_cap")
        context_length = pipe.get("context_length")  # None if not provided (V1 compatibility)
        overlap = pipe.get("overlap")  # None if not provided (V1 compatibility)
        skip_first_frames = pipe.get("skip_first_frames")
        select_every_nth = pipe.get("select_every_nth")
        batch_size = pipe.get("batch_size")
        path = pipe.get("path") or ""

        # Generate latent with defaults if dimensions/batch_size are None
        latent_width = width if width is not None else 576
        latent_height = height if height is not None else 1024
        latent_batch_size = batch_size if batch_size is not None else 1
        
        output_latent = self.generate(latent_width, latent_height, latent_batch_size)[0]

        return (width, height, frame_rate, frame_load_cap, context_length, overlap, skip_first_frames, select_every_nth, output_latent, path)

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