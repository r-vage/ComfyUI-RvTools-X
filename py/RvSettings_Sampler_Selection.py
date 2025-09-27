# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import comfy
from ..core import CATEGORY, SAMPLERS_COMFY, SCHEDULERS_ANY
from typing import Any, Dict, List, Tuple

class RvSettings_Sampler_Selection:
    CATEGORY = CATEGORY.MAIN.value + CATEGORY.SETTINGS.value
    RETURN_TYPES = ("pipe",)
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        return {
            "required": {
                "Sampler": (SAMPLERS_COMFY, {"tooltip": "Select the sampler algorithm."}),
                "Scheduler": (SCHEDULERS_ANY, {"tooltip": "Select the scheduler algorithm."}),
            },
        }

    def execute(
        self,
        Sampler: str,
        Scheduler: str
    ) -> Tuple[List[Any]]:
        pipe = {
            "sampler": Sampler,
            "scheduler": Scheduler,
        }
        return (pipe,)

NODE_NAME = 'Sampler Selection [RvTools-X]'
NODE_DESC = 'Sampler Selection'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvSettings_Sampler_Selection
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
