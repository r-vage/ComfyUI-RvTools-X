# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from __future__ import annotations
from ..core import CATEGORY, purge_vram

class RvSwitch_Multi_Model:
    @classmethod
    def INPUT_TYPES(cls):
        # Only inputcount is required; model inputs are optional so validation doesn't fail
        # when some inputs are intentionally left empty or bypassed.
        return {
            "required": {
                "inputcount": ("INT", {"default": 2, "min": 1, "max": 64, "step": 1, "tooltip": "Number of model inputs to expose; click 'Update inputs' to add or remove inputs."}),
                "Purge_VRAM": ("BOOLEAN", {"default": False, "tooltip": "If enabled, purges VRAM and unloads all models before switching. Use when swapping large models to avoid OOM."}),
            },
            "optional": {
                "model_1": ("MODEL", {"tooltip": "Model input #1 (highest priority). Leave empty to bypass."}),
                "model_2": ("MODEL", {"tooltip": "Model input #2 (used if #1 is empty)."}),
            }
        }

    RETURN_TYPES = ("MODEL",)
    RETURN_NAMES = ("model",)
    FUNCTION = "select"
    CATEGORY = CATEGORY.MAIN.value +  CATEGORY.MULTISWITCHES.value
    DESCRIPTION = "Multi-switch for MODEL inputs. Click 'Update inputs' (frontend) to add/remove model_X inputs. The node returns the first connected/non-None model in numeric order."


    def select(self, inputcount, Purge_VRAM=False, **kwargs):
        # Helper to detect empty/bypassed values commonly produced by ComfyUI flows
        def _is_empty(v):
            # None is empty
            if v is None:
                return True
            # Empty tuple/list is empty
            if isinstance(v, (tuple, list)) and len(v) == 0:
                return True
            # Tuple/list of only Nones is empty
            if isinstance(v, (tuple, list)) and all(x is None for x in v):
                return True
            # Empty dict-like
            if isinstance(v, dict) and len(v) == 0:
                return True
            # Empty or whitespace-only string
            if isinstance(v, str) and v.strip() == "":
                return True
            # If it's a container where all elements are falsy, treat as empty
            if isinstance(v, (tuple, list, set)) and all(not bool(x) for x in v):
                return True
            # Otherwise consider it non-empty
            return False

        # Optionally purge VRAM before switching
        if Purge_VRAM:
            purge_vram()

        # Look through model_1 .. model_N and return first non-empty value
        for i in range(1, max(1, inputcount) + 1):
            key = f"model_{i}"
            val = kwargs.get(key)
            if not _is_empty(val):
                return (val,)

        # Nothing provided — raise a clear error so the user can fix the workflow
        raise RuntimeError(
            f"RvMSwitch_Model_v2: no model found among model_1..model_{inputcount}. "
            "Please connect at least one MODEL input or reduce inputcount."
        )


NODE_NAME = 'Model Multi-Switch [RvTools-X]'
NODE_DESC = 'Model Multi-Switch'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvSwitch_Multi_Model
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}