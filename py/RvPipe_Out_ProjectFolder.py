# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import torch
import comfy.model_management
from ..core import CATEGORY

class RvPipe_Out_ProjectFolder:
    def __init__(self):
        self.device = comfy.model_management.intermediate_device()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pipe": ("pipe", {"tooltip": "Input pipe containing path, width, height and batch_size (dict or tuple)."}),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PIPE.value
    RETURN_TYPES = ("INT",   "INT",    "INT",        "LATENT", "STRING")
    RETURN_NAMES = ("width", "height", "batch_size", "latent", "path")
    FUNCTION = "execute"

    def execute(self, pipe=None) -> tuple:
        # Only accept dict-style pipes now.
        if pipe is None:
            raise ValueError("Input pipe must not be None and must be a dict-style pipe")
        if not isinstance(pipe, dict):
            raise ValueError("RvPipe_Out_ProjectFolder expects dict-style pipes only.")

        path = pipe.get("path") or ""
        try:
            width = int(pipe.get("width")) if pipe.get("width") is not None else 0
        except Exception:
            width = 0
        try:
            height = int(pipe.get("height")) if pipe.get("height") is not None else 0
        except Exception:
            height = 0
        try:
            batch_size = int(pipe.get("batch_size")) if pipe.get("batch_size") is not None else 1
        except Exception:
            batch_size = 1

        # Generate latent with the given width and height
        output_latent = self.generate(width, height, batch_size)[0]

        return (width, height, batch_size, output_latent, path)

    def generate(self, width, height, batch_size=1):
        latent = torch.zeros([batch_size, 4, height // 8, width // 8], device=self.device)
        return ({"samples":latent},)
                

NODE_NAME = 'Pipe Out Project Folder [RvTools-X]'
NODE_DESC = 'Pipe Out Project Folder'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvPipe_Out_ProjectFolder
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
