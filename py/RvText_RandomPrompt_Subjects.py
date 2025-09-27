# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import json
import os
import random
import re

from ..core import CATEGORY, cstr

class RvText_RandomPrompt:
    def __init__(self):
        self.last_seed = None
        self.last_output = None
        self.file_options = None

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.TEXT.value
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "create_prompt"

    @classmethod
    def INPUT_TYPES(cls):
        required = {}
        # Only load files matching 0_0Name.txt pattern in json/subjects
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
        subjects_dir = os.path.join(parent_dir, 'json', 'subjects')
        if not os.path.isdir(subjects_dir):
            os.makedirs(subjects_dir, exist_ok=True)
        for fname in os.listdir(subjects_dir):
            if fname.lower().endswith('.txt') and re.match(r'^\d+_\d+\w+\.txt$', fname):
                base = os.path.splitext(fname)[0]
                display = re.sub(r'^[0-9_]+', '', base)
                fpath = os.path.join(subjects_dir, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        lines = [line.strip() for line in f if line.strip()]
                        combo_options = ['None', 'Random'] + lines
                        required[display] = (tuple(combo_options), {"default": "None", "tooltip": f"Select entry from {fname}"})
                except Exception:
                    required[display] = (('None',), {"default": "None", "tooltip": f"Select entry from {fname}"})
        return {
            "required": required,
            "optional": {
                "seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 1125899906842624}),
            }
        }

    def create_prompt(self, **kwargs):
        # Build prompt from selected or random lines
        if "seed" not in kwargs:
            raise ValueError("Error: No seed provided to RandomPrompt node. Please connect a seed input.")
        seed = kwargs.get("seed", 0)
        if self.last_seed == seed and self.last_output is not None:
            return (self.last_output,)
        # Scan files in json/subjects
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
        subjects_dir = os.path.join(parent_dir, 'json', 'subjects')
        file_map = {}
        for fname in os.listdir(subjects_dir):
            if fname.lower().endswith('.txt') and re.match(r'^\d+_\d+\w+\.txt$', fname):
                base = os.path.splitext(fname)[0]
                display = re.sub(r'^[0-9_]+', '', base)
                fpath = os.path.join(subjects_dir, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        lines = [line.strip() for line in f if line.strip()]
                        file_map[display] = lines
                except Exception:
                    file_map[display] = []
        values = []
        random.seed(seed)
        for display, lines in file_map.items():
            val = kwargs.get(display, "None")
            if val == "Random":
                if lines:
                    selected = random.choice(lines)
                    values.append(selected)
            elif val not in ("None", "disabled"):
                values.append(val.strip())
        prompt = ','.join(values).strip()
        prompt = re.sub(r"[\r\n]+", " ", prompt)
        prompt += ',' if prompt else ''
        self.last_seed = seed
        self.last_output = prompt
        return (prompt,)

NODE_NAME = 'Random Prompt by jice: Subjects [RvTools-X]'
NODE_DESC = 'Random Prompt (Subjects)'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvText_RandomPrompt
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}