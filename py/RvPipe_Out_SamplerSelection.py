# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, AnyType

any = AnyType("*")

class RvPipe_Out_SamplerSelection:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pipe": ("pipe", {"tooltip": "Input dict-style pipe containing sampler and scheduler."}),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PIPE.value
    RETURN_TYPES = (any, any)
    RETURN_NAMES = ("sampler", "scheduler")
    FUNCTION = "execute"

    def execute(self, pipe: dict = None) -> tuple:
        # Only accept dict-style pipes now.
        if pipe is None:
            raise ValueError("Input pipe must not be None and must be a dict-style pipe")
        if not isinstance(pipe, dict):
            raise ValueError("RvPipe_Out_SamplerSelection expects dict-style pipes only.")

        sampler = pipe.get("sampler") or pipe.get("sampler_name") or None
        scheduler = pipe.get("scheduler") or pipe.get("scheduler_name") or None

        return (sampler, scheduler)

NODE_NAME = 'Pipe Out Sampler Selection [RvTools-X]'
NODE_DESC = 'Pipe Out Sampler Selection'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvPipe_Out_SamplerSelection
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}