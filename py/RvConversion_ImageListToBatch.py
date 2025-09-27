# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import torch
import torchvision.transforms.v2 as T

from ..core import CATEGORY

def p(image):
    return image.permute([0,3,1,2])
def pb(image):
    return image.permute([0,2,3,1])


class RvConversion_ImageListToBatch:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.CONVERSION.value
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    INPUT_IS_LIST = True

    FUNCTION = "execute"

    def execute(self, images):
        if images is None:
            raise ValueError("Input 'images' cannot be None.")
        if isinstance(images, torch.Tensor) and images.ndim == 4:
            if images.shape[0] > 0:
                return (images,)
            else:
                raise ValueError("Input batch tensor cannot be empty.")
        if not isinstance(images, (list, tuple)):
            raise TypeError("Input 'images' must be a list, tuple, or batch tensor.")
        if len(images) == 0:
            raise ValueError("Input 'images' cannot be an empty list or tuple.")
        try:
            shape = images[0].shape[1:3]
            out = []
            for i, img_in in enumerate(images):
                if not hasattr(img_in, "shape") or img_in.ndim < 3:
                    raise TypeError(f"Image at index {i} is not a valid tensor.")
                img = p(img_in)
                if img_in.shape[1:3] != shape:
                    transforms = T.Compose([
                        T.CenterCrop(min(img.shape[2], img.shape[3])),
                        T.Resize((shape[0], shape[1]), interpolation=T.InterpolationMode.BICUBIC),
                    ])
                    img = transforms(img)
                out.append(pb(img))
            out = torch.cat(out, dim=0)
            return (out,)
        except Exception as e:
            raise RuntimeError(f"Image list to batch conversion failed: {e}")

NODE_NAME = 'Imagelist to Batch [RvTools-X]'
NODE_DESC = 'Imagelist to Batch'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvConversion_ImageListToBatch
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}