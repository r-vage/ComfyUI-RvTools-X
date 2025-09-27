# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import torch
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

class RvConversion_MaskBatchToList:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "masks": ("MASK", {}, "Input must be a non-empty mask batch tensor (shape [N,...]) or a non-empty mask list/tuple. If input is a mask list/tuple, it is returned unchanged. If input is a mask batch tensor, it is split into a mask list. Empty or None input is not allowed."),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.CONVERSION.value
    RETURN_TYPES = ("MASK", )
    OUTPUT_IS_LIST = (True, )

    FUNCTION = "execute"

    def execute(self, masks):
#
#         Converts a non-empty mask batch tensor to a list of masks, or returns a non-empty mask list/tuple unchanged.
#         Raises ValueError/TypeError for invalid input.
#
        if masks is None:
            raise ValueError("Input 'masks' cannot be None.")
        if isinstance(masks, (list, tuple)):
            if len(masks) == 0:
                raise ValueError("Input 'masks' cannot be an empty list or tuple.")
            # Validate each mask is a tensor with shape
            for i, m in enumerate(masks):
                if not hasattr(m, "shape") or m.ndim < 2:
                    raise TypeError(f"Mask at index {i} is not a valid tensor.")
            return (list(masks),)
        if hasattr(masks, "shape") and hasattr(masks, "__getitem__"):
            batch_size = masks.shape[0]
            if batch_size == 0:
                raise ValueError("Input mask batch cannot be empty.")
            # Use list comprehension for performance and validate each mask
            mask_list = []
            for i in range(batch_size):
                m = make_3d_mask(masks[i])
                if not hasattr(m, "shape") or m.ndim < 2:
                    raise TypeError(f"Mask at batch index {i} is not a valid tensor.")
                mask_list.append(m)
            return (mask_list,)
        raise TypeError("Input 'masks' must be a mask batch tensor or a non-empty list/tuple of masks.")

NODE_NAME = "Maskbatch to List [RvTools-X]"
NODE_DESC = "Maskbatch to List"

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvConversion_MaskBatchToList
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}