# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import os
import numpy as np
from PIL import Image
import torch
from typing import Union, List
import subprocess

from ..core import CATEGORY, cstr

try:
    import pilgram
except ImportError:
    subprocess.check_call(['pip', 'install', 'pilgram'])
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

class RvImage_Style:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", {"tooltip": "Batch of images to style."}),
                "style": (["1977", "aden", "brannan", "brooklyn", "clarendon", "earlybird", "gingham", "hudson", "inkwell", "kelvin", "lark", "lofi", "maven", "mayfair", "moon", "nashville", "perpetua", "reyes", "rise", "slumber", "stinson", "toaster", "valencia", "walden", "willow", "xpro2"], {"tooltip": "Instagram-like style filter to apply."}),
            },
            "optional": {
                "All": ("BOOLEAN", {"default": False, "tooltip": "Apply all styles to each image."}),
            },
        }
    
    CATEGORY = CATEGORY.MAIN.value + CATEGORY.IMAGE.value

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"
    

    def execute(self, image, style, All=False):
#
#         Applies Instagram-like style filters to images using pilgram.
#         Handles None and empty input robustly.
#
        # Type safety: ensure valid images and parameters
        if image is None or not hasattr(image, '__iter__') or len(image) == 0:
            return (torch.empty(0),)
        if not isinstance(style, str) or not style:
            style = "1977"
        if not isinstance(All, bool):
            All = False

        style_map = {
            "1977": pilgram._1977,
            "aden": pilgram.aden,
            "brannan": pilgram.brannan,
            "brooklyn": pilgram.brooklyn,
            "clarendon": pilgram.clarendon,
            "earlybird": pilgram.earlybird,
            "gingham": pilgram.gingham,
            "hudson": pilgram.hudson,
            "inkwell": pilgram.inkwell,
            "kelvin": pilgram.kelvin,
            "lark": pilgram.lark,
            "lofi": pilgram.lofi,
            "maven": pilgram.maven,
            "mayfair": pilgram.mayfair,
            "moon": pilgram.moon,
            "nashville": pilgram.nashville,
            "perpetua": pilgram.perpetua,
            "reyes": pilgram.reyes,
            "rise": pilgram.rise,
            "slumber": pilgram.slumber,
            "stinson": pilgram.stinson,
            "toaster": pilgram.toaster,
            "valencia": pilgram.valencia,
            "walden": pilgram.walden,
            "willow": pilgram.willow,
            "xpro2": pilgram.xpro2,
        }

        tensors = []
        if All:
            for img in image:
                for filter_name, filter_func in style_map.items():
                    tensors.append(pil2tensor(filter_func(tensor2pil(img))))
            tensors = torch.cat(tensors, dim=0)
            return (tensors,)
        else:
            for img in image:
                filter_func = style_map.get(style, lambda x: x)
                styled_img = pil2tensor(filter_func(tensor2pil(img))) if style in style_map else img
                tensors.append(styled_img)
            tensors = torch.cat(tensors, dim=0)
            return (tensors,)

NODE_NAME = 'Image Style [RvTools-X]'
NODE_DESC = 'Image Style'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvImage_Style
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}