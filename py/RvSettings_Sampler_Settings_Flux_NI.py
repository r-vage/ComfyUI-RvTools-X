# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import comfy
import comfy.sd
import folder_paths
from ..core import CATEGORY, SAMPLERS_COMFY, SCHEDULERS_ANY
from typing import Any, Dict, List, Tuple

class RvSettings_Sampler_Settings_Flux_NI:
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
                "Flux_Guidance": ("FLOAT", {"default": 3.50, "min": 0.00, "step": 0.01, "tooltip": "Flux guidance scale."}),
                "Denoise": ("FLOAT", {"default": 1.0, "min": 0.00, "max": 1.0, "step": 0.10, "tooltip": "Denoise strength (0-1)."}),
                "Sigmas_Denoise": ("FLOAT", {"default": 0.45, "min": 0.00, "step": 0.01, "tooltip": "Sigma denoise value."}),
                "Noise_Strength": ("FLOAT", {"default": 0.50, "min": 0.00, "step": 0.01, "tooltip": "Noise strength value."}),
            },
        }

    def execute(
        self,
        Sampler: str,
        Scheduler: str,
        Steps: int,
        CFG: float,
        Flux_Guidance: float,
        Denoise: float,
        Sigmas_Denoise: float,
        Noise_Strength: float,
    ) -> Tuple:
        pipe = {
            "sampler": Sampler,
            "scheduler": Scheduler,
            "steps": int(Steps),
            "cfg": float(CFG),
            "guidance": float(Flux_Guidance),
            "denoise": float(Denoise),
            "sigmas_denoise": float(Sigmas_Denoise),
            "noise_strength": float(Noise_Strength),
            "seed": int(0),
        }
        return (pipe,)

NODE_NAME = 'Sampler Settings NI (Flux) [RvTools-X]'
NODE_DESC = 'Sampler Settings NI (Flux)'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvSettings_Sampler_Settings_Flux_NI
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
