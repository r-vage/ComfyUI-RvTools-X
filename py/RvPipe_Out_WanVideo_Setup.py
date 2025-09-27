# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY

class RvPipe_Out_WanVideo_Setup:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pipe": ("pipe", {"tooltip": "Input dict-style pipe containing steps, cfg, model_shift, steps_start, and steps_stop."}),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PIPE.value
    RETURN_TYPES = ("INT", "FLOAT", "FLOAT", "INT", "INT")
    RETURN_NAMES = ("steps", "cfg", "model_shift", "steps_start", "steps_stop")
    FUNCTION = "execute"

    def execute(self, pipe: dict = None) -> tuple:
        # Only accept dict-style pipes now.
        if pipe is None:
            raise ValueError("Input pipe must not be None and must be a dict-style pipe")
        if not isinstance(pipe, dict):
            raise ValueError("RvPipe_Out_WvW_Setup expects dict-style pipes only.")

        try:
            steps = int(pipe.get("steps")) if pipe.get("steps") is not None else 0
        except Exception:
            steps = 0
        try:
            cfg = float(pipe.get("cfg")) if pipe.get("cfg") is not None else 0.0
        except Exception:
            cfg = 0.0
        try:
            model_shift = float(pipe.get("model_shift")) if pipe.get("model_shift") is not None else 0.0
        except Exception:
            model_shift = 0.0
        try:
            steps_start = int(pipe.get("steps_start")) if pipe.get("steps_start") is not None else 0
        except Exception:
            steps_start = 0
        try:
            steps_stop = int(pipe.get("steps_stop")) if pipe.get("steps_stop") is not None else 0
        except Exception:
            steps_stop = 0

        return (steps, cfg, model_shift, steps_start, steps_stop)

NODE_NAME = 'Pipe Out WanVideo Setup [RvTools-X]'
NODE_DESC = 'Pipe Out WanVideo Setup'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvPipe_Out_WanVideo_Setup
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}