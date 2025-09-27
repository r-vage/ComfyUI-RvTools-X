# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import json
import os
import random
import re

from ..core import CATEGORY, cstr

class RvText_Prompt_Settings_Slider:
    JSON_FILE_PATH = 'settings.json'
    CATEGORY_KEYS = [
        'Shotstyle 1', 'Shotstyle 2', 'Artists', 'Arists Special', 'Film Directors', 'Architects',
        'Photography Styles', 'Lighting', 'Effects', 'Magic Elements', 'Camera', 'Films', 'Image Type',
        'Composition Method', 'Art Style', 'Art Style+', 'Scene Atmosphere', 'Theme', 'Printing Materials',
        'Illustration Style', 'Color Theme'
    ]

    def __init__(self):
        self.options = {}
        self.load_json()

    def load_json(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
        json_dir = os.path.join(parent_dir, 'json')
        json_file_path = os.path.join(json_dir, self.JSON_FILE_PATH)
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                self.options = json.load(f)
        except Exception as e:
            cstr(f"Error reading JSON file: {e}").error.print()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                **cls.get_input_types_from_keys(cls.CATEGORY_KEYS),
                "seed": ("INT", {"default": 0, "min": -1125899906842624, "max": 1125899906842624, "tooltip": "Random seed for settings selection."}),
            }
        }

    @staticmethod
    def get_input_types_from_keys(keys):
        input_types = {}
        for key in keys:
            input_types[key] = (
                tuple(RvText_Prompt_Settings_Slider.get_options_keys(key)),
                {
                    "default": "None",
                    "tooltip": f"Select {key} settings option."
                }
            )
            input_types[f"{key}weight"] = (
                "FLOAT",
                {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 1.4,
                    "step": 0.1,
                    "display": "slider",
                    "tooltip": f"Weight for {key} (1.0 = normal, >1 = stronger)."
                }
            )
        return input_types

    @staticmethod
    def get_options_keys(key):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
        json_dir = os.path.join(parent_dir, 'json')
        json_file_path = os.path.join(json_dir, RvText_Prompt_Settings_Slider.JSON_FILE_PATH)
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                options = json.load(f)
                return list(options[key].keys())
        except Exception:
            return ["None"]

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.TEXT.value
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "execute"

    def execute(self, **kwargs) -> tuple[str]:
        prompt_parts: dict[str, str] = {}
        for key in self.CATEGORY_KEYS:
            value = kwargs.get(key, "None")
            if value in self.options.get(key, {}) and value != "None":
                weight_key = f"{key}weight"
                weight = kwargs.get(weight_key, 1.0)
                if value == "Random":
                    choices = [k for k in self.options[key].keys() if k not in ("None", "Random")]
                    if choices:
                        selected = random.choice(choices)
                        part = self.options[key][selected]
                    else:
                        part = ""
                else:
                    part = self.options[key][value]
                if part:
                    if weight != 1:
                        prompt_parts[key] = f"({part}:{weight:.1f})"
                    else:
                        prompt_parts[key] = part
        prompt = ','.join(prompt_parts.values()).strip()
        # Replace all line breaks with spaces for prompt output
        prompt = re.sub(r"[\r\n]+", " ", prompt)
        prompt += ',' if prompt else ''
        return (prompt,) if prompt else ('',)

NODE_NAME = 'Prompt Settings Slider [RvTools-X]'
NODE_DESC = 'Prompt Settings Slider'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvText_Prompt_Settings_Slider
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
