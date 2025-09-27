# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from typing import Any, Dict
from ..core import CATEGORY

class RvConversion_ConcatMulti:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "inputcount": ("INT", {"default": 2, "min": 2, "max": 256, "step": 1}),
                "pipe_1": ("pipe",),
            },
            "optional": {
                "pipe_2": ("pipe",),
                "merge_strategy": (["overwrite", "preserve", "merge"], {"default": "merge"}),
            },
        }

    RETURN_TYPES = ("pipe",)
    RETURN_NAMES = ("pipe",)
    FUNCTION = "concat"
    CATEGORY = CATEGORY.MAIN.value + CATEGORY.CONVERSION.value

    DESCRIPTION = "Merge multiple pipe/context inputs into a single context dict pipe."

    # keys that should be treated as list-like when merging
    _KNOWN_LIST_KEYS = {"images", "images_pp", "mask", "lora_names", "loras", "embeddings", "positive_list", "negative_list"}

    def concat(self, inputcount: int = 2, merge_strategy: str = "merge", **kwargs) -> tuple:
        result: Dict[str, Any] = {}

        aliases = {
            "Steps": "steps",
            "CFG": "cfg",
            "model_name": "model_name",
            "lora_names": "lora_names",
            "loras": "lora_names",
            "seed": "seed",
            "sampler_name": "sampler_name",
            "vae_name": "vae_name",
            "directory": "path",
        }

        def set_value(k, v):
            # helper to set value into result respecting strategy
            if merge_strategy == "preserve":
                if k in result and result[k] not in (None, ""):
                    return
                result[k] = v
                return

            if merge_strategy == "merge":
                if k in result:
                    existing = result[k]
                    # Special case for comma-separated strings in known list keys
                    if k in self._KNOWN_LIST_KEYS and isinstance(existing, str) and isinstance(v, str):
                        result[k] = existing + ", " + v
                        return
                    # if either is list/tuple, concatenate
                    if isinstance(existing, (list, tuple)) or isinstance(v, (list, tuple)) or k in self._KNOWN_LIST_KEYS:
                        existing_list = list(existing) if not isinstance(existing, list) else existing
                        new_list = list(v) if isinstance(v, (list, tuple)) else [v]
                        result[k] = existing_list + new_list
                        return
                # fallback to overwrite
                result[k] = v
                return

            # default overwrite
            result[k] = v

        for idx in range(1, inputcount + 1):
            pipe = kwargs.get(f"pipe_{idx}")
            if pipe is None:
                continue

            # only accept dict-style pipes (tuples removed by design)
            if not isinstance(pipe, dict):
                raise ValueError(
                    "RvPipe_ConcatMulti expects dict-style pipes only. Convert tuples to dicts before concatenating."
                )

            ctx = pipe

            for k, v in ctx.items():
                # skip None/empty values when merging preserve/overwrite
                if v is None:
                    continue

                # canonicalize common alias keys to a single repo-wide name
                key = aliases.get(k, k)

                # normalize simple list-like values to list when merge is used (but keep strings for concatenation)
                if merge_strategy == "merge" and key in self._KNOWN_LIST_KEYS and not isinstance(v, (list, tuple)) and not isinstance(v, str):
                    v = [v]

                set_value(key, v)

        # Ensure the result always contains a pipe key for convenience
        if "pipe" not in result:
            result["pipe"] = result

        return (result,)

NODE_NAME = 'Concat Pipe Multi [RvTools-X]'
NODE_DESC = 'Concat Pipe Multi'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvConversion_ConcatMulti
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}