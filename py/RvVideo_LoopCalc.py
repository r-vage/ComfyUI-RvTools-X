# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import sys
import math
from typing import Tuple
import torch

from ..core import CATEGORY, cstr

class RvVideo_LoopCalc:
#     Calculates required number of loops for processing frames with overlap
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "total_frames": ("INT", {"default": 16, "min": 1, "max": 10000, "step": 1, "tooltip": "Total number of frames in the video."}),
                "context_length": ("INT", {"default": 8, "min": 1, "max": 32, "step": 1, "tooltip": "Context length for frame calculation."}),
                "overlap_frames": ("INT", {"default": 4, "min": 0, "max": 32, "step": 1, "tooltip": "Number of overlapping frames between contexts."}),
                "images": ("IMAGE", {"tooltip": "Batch of images to process."}),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.VIDEO.value

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("total_loops",)
    
    FUNCTION = "calculate"

    def calculate(self, total_frames: int, context_length: int, overlap_frames: int, images) -> Tuple[int]:
        # Calculates the required number of loops for processing frames with overlap in video workflows.
        # Handles None and empty input robustly.
        for name, val, default in [
            ("total_frames", total_frames, 16),
            ("context_length", context_length, 8),
            ("overlap_frames", overlap_frames, 4)
        ]:
            if not isinstance(val, int):
                locals()[name] = default

        try:
            image_count = 0
            if isinstance(images, torch.Tensor) and images.ndim > 0:
                image_count = int(images.shape[0])

            remaining_frames = max(0, total_frames - image_count)
            effective_stride = max(1, context_length - overlap_frames)
            total_loops = math.ceil(remaining_frames / effective_stride) if remaining_frames > 0 else 0
            result = max(1, int(total_loops))
            return (result,)
        except Exception as e:
            cstr(f"Loop calculation failed: {str(e)}").error.print()
            return (1,)

NODE_NAME = 'Loop Calculator [RvTools-X]'
NODE_DESC = 'Loop Calculator'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvVideo_LoopCalc
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}