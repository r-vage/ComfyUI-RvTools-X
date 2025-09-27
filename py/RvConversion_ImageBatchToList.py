# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY

class RvConversion_ImageBatchToList:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", {},
                    "Image batch (e.g. numpy/tensor, shape [N,...]).\nReturns a list of single-image batches.")
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.CONVERSION.value
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    OUTPUT_IS_LIST = (True,)

    FUNCTION = "execute"

    def execute(self, images):
        if images is None:
            raise ValueError("Input 'images' cannot be None.")
        if isinstance(images, (list, tuple)):
            if len(images) == 0:
                raise ValueError("Input 'images' cannot be an empty list or tuple.")
            # Validate each image is a tensor with shape
            for i, img in enumerate(images):
                if not hasattr(img, "shape") or img.ndim < 3:
                    raise TypeError(f"Image at index {i} is not a valid tensor.")
            return (list(images),)
        if not hasattr(images, "shape") or not hasattr(images, "__getitem__"):
            raise TypeError("Input 'images' must be a batch tensor or a list/tuple of images.")
        try:
            batch_size = images.shape[0]
            if batch_size == 0:
                raise ValueError("Input batch tensor cannot be empty.")
            # Validate each image in batch
            img_list = []
            for i in range(batch_size):
                img = images[i:i + 1, ...]
                if not hasattr(img, "shape") or img.ndim < 3:
                    raise TypeError(f"Image at batch index {i} is not a valid tensor.")
                img_list.append(img)
            return (img_list,)
        except Exception as e:
            raise RuntimeError(f"Image batch to list conversion failed: {e}")

NODE_NAME = "Imagebatch to List [RvTools-X]"
NODE_DESC = "Imagebatch to List"

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvConversion_ImageBatchToList
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}