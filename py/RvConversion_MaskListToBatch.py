# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import torch
import comfy
from ..core import CATEGORY

def make_3d_mask(mask):
    # Type safety: handle missing shape
    if not hasattr(mask, "shape"):
        return mask
    if len(mask.shape) == 4:
        return mask.squeeze(0)
    elif len(mask.shape) == 2:
        return mask.unsqueeze(0)
    return mask

class RvConversion_MaskListToBatch:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask": ("MASK", {}, "Input must be a non-empty mask list or tuple. Returns a single mask batch tensor. Masks are upscaled to match the first mask's shape. Empty or None input is not allowed."),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.CONVERSION.value
    RETURN_TYPES = ("MASK", )
    INPUT_IS_LIST = True

    FUNCTION = "execute"

    def execute(self, mask):
#
#         Converts a non-empty mask list/tuple to a batch tensor, upscaling masks as needed.
#         If input is already a mask batch tensor, returns it unchanged.
#         Raises ValueError/TypeError for invalid input.
#
        if mask is None:
            raise ValueError("Input 'mask' cannot be None.")
        if isinstance(mask, torch.Tensor) and mask.ndim in (3, 4):
            if mask.shape[0] > 0:
                return (mask,)
            else:
                raise ValueError("Input mask batch cannot be empty.")
        if not isinstance(mask, (list, tuple)):
            raise TypeError("Input 'mask' must be a list, tuple, or mask batch tensor.")
        if len(mask) == 0:
            raise ValueError("Input 'mask' cannot be an empty list or tuple.")
        try:
            # Convert all masks to 3D and upscale if needed
            ref_shape = None
            mask_tensors = []
            for i, m in enumerate(mask):
                m3d = make_3d_mask(m)
                if not hasattr(m3d, "shape") or m3d.ndim != 3:
                    raise TypeError(f"Mask at index {i} is not a valid 3D tensor.")
                if ref_shape is None:
                    ref_shape = m3d.shape[1:]
                elif m3d.shape[1:] != ref_shape:
                    # Upscale to match reference shape
                    m3d = comfy.utils.common_upscale(m3d.movedim(-1, 1), ref_shape[1], ref_shape[0], "lanczos", "center").movedim(1, -1)
                mask_tensors.append(m3d)
            # Stack all masks into batch tensor
            batch = torch.stack(mask_tensors, dim=0)
            return (batch,)
        except Exception as e:
            raise RuntimeError(f"Mask list to batch conversion failed: {e}")

NODE_NAME = "Masklist to Batch [RvTools-X]"
NODE_DESC = "Masklist to Batch"

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvConversion_MaskListToBatch
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}