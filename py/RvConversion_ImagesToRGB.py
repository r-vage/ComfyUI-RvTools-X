# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import torch
import numpy as np

from PIL import Image
from ..core import CATEGORY

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)


class RvConversion_ImagesToRGB:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
            },
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.CONVERSION.value
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)

    FUNCTION = "execute"

    def execute(self, images):
        if images is None:
            raise ValueError("Input 'images' cannot be None.")

        def is_rgb_tensor(img):
            return isinstance(img, torch.Tensor) and img.ndim == 4 and img.shape[1] == 3

        def convert_to_rgb(img):
            if is_rgb_tensor(img):
                return img
            pil_img = tensor2pil(img) if isinstance(img, torch.Tensor) else img
            rgb_pil = pil_img.convert('RGB')
            return pil2tensor(rgb_pil)

        # Single image (PIL)
        if isinstance(images, Image.Image):
            return (convert_to_rgb(images), )

        # Batch tensor or single image tensor
        if isinstance(images, torch.Tensor):
            if is_rgb_tensor(images):
                return (images, )
            if images.ndim == 4:
                # Convert each image in batch
                tensors = [convert_to_rgb(images[i]) for i in range(images.shape[0])]
                tensors = torch.cat(tensors, dim=0)
                return (tensors, )
            # Single image tensor (shape [C, H, W])
            return (convert_to_rgb(images), )

        # List/tuple of images
        if not isinstance(images, (list, tuple)):
            raise TypeError("Input 'images' must be a list, tuple, tensor, or PIL.Image.")
        if len(images) == 0:
            raise ValueError("Input 'images' cannot be an empty list or tuple.")

        # If all images are already RGB tensors, return input as-is
        if all(is_rgb_tensor(img) for img in images):
            return (torch.cat(images, dim=0) if len(images) > 1 else images[0], )

        # Otherwise, convert only those that need conversion
        tensors = [convert_to_rgb(img) for img in images]
        tensors = torch.cat(tensors, dim=0)
        return (tensors, )

NODE_NAME = 'Image to RGB [RvTools-X]'
NODE_DESC = 'Image to RGB'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvConversion_ImagesToRGB
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}