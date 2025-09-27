# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import comfy
import comfy.sd
import folder_paths
from ..core import CATEGORY, SAMPLERS_COMFY, SCHEDULERS_ANY
from typing import Any, Dict, List, Tuple

class RvSettings_Sampler_Settings_Small:
    CATEGORY = CATEGORY.MAIN.value + CATEGORY.SETTINGS.value
    RETURN_TYPES = ("pipe",)
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        return {
            "required": {
                "Sampler": (SAMPLERS_COMFY, {"tooltip": "Select the sampler algorithm."}),
                "Scheduler": (SCHEDULERS_ANY, {"tooltip": "Select the scheduler algorithm."}),
                "Steps": ("INT", {"default": 20, "min": 1, "step": 1, "tooltip": "Number of sampling steps."}),
                "CFG": ("FLOAT", {"default": 3.50, "min": 0.00, "step": 0.01, "tooltip": "Classifier-Free Guidance scale."}),
            },
        }

    def execute(
        self,
        Sampler: str,
        Scheduler: str,
        Steps: int,
        CFG: float
    ) -> Tuple:
        pipe = {
            "sampler": Sampler,
            "scheduler": Scheduler,
            "steps": int(Steps),
            "cfg": float(CFG),
        }
        return (pipe,)

NODE_NAME = 'Sampler Settings Small [RvTools-X]'
NODE_DESC = 'Sampler Settings Small'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvSettings_Sampler_Settings_Small
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
