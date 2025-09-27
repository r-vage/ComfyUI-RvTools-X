# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import comfy
import comfy.sd
from ..core import CATEGORY, cstr
from ..core import AnyType

any = AnyType("*")

# original code is taken from rgthree context utils
_all_context_input_output_data = {
    "pipe": ("pipe", "pipe", "context"),
    "model": ("model", "MODEL", "model"),
    "clip": ("clip", "CLIP", "clip"),
    "vae": ("vae", "VAE", "vae"),
    "positive": ("positive", "CONDITIONING", "positive"),
    "negative": ("negative", "CONDITIONING", "negative"),
    "latent": ("latent", "LATENT", "latent"),
    "images": ("images", "IMAGE", "images"),
    "images_pp": ("images_pp", "IMAGE", "images_pp"),
    "mask": ("mask", "MASK", "mask"),    
    "sampler": ("sampler", any, "sampler"),
    "scheduler": ("scheduler", any, "scheduler"),
    "steps": ("steps", "INT", "steps"),
    "cfg": ("cfg", "FLOAT", "cfg"),
    "guidance": ("guidance", "FLOAT", "guidance"),
    "seed": ("seed", "INT", "seed"),
    "width": ("width", "INT", "width"),
    "height": ("height", "INT", "height"),
    "batch_size": ("batch_size", "INT", "batch_size"),
    "text_pos": ("text_pos", "STRING", "text_pos"),
    "text_pos_i2p": ("text_pos_i2p", "STRING", "text_pos_i2p"),
    "text_neg": ("text_neg", "STRING", "text_neg"),

    "frame_rate": ("frame_rate", "FLOAT", "frame_rate"),
    "frame_load_cap": ("frame_load_cap", "INT", "frame_load_cap"),
    "skip_first_frames": ("skip_first_frames", "INT", "skip_first_frames"),
    "select_every_nth": ("select_every_nth", "INT", "select_every_nth"),
    "images_input": ("images_input", "IMAGE", "images_input"),
    "images_ref_start": ("images_ref_start", "IMAGE", "images_ref_start"),
    "images_ref_end": ("images_ref_end", "IMAGE", "images_ref_end"),
    "images_output": ("images_output", "IMAGE", "images_output"),
    "audio_input": ("audio_input", "AUDIO", "audio_input"),
    "audio_output": ("audio_output", "AUDIO", "audio_output"),

    "any_1": ("any_1", any, "any_1"),
    "any_2": ("any_2", any, "any_2"),
    "any_3": ("any_3", any, "any_3"),
    "any_4": ("any_4", any, "any_4"),
    "any_5": ("any_5", any, "any_5"),
    "any_6": ("any_6", any, "any_6"),
    "any_7": ("any_7", any, "any_7"),
    "any_8": ("any_8", any, "any_8"),

    "path": ("path", "STRING", "path"),
}

force_input_types = ["INT", "STRING", "FLOAT"]
force_input_names = ["sampler", "scheduler"]

def _create_context_data(input_list=None):
    # Returns a tuple of context inputs, return types, and return names to use in a node's def.
    if input_list is None:
        input_list = _all_context_input_output_data.keys()
    list_ctx_return_types = []
    list_ctx_return_names = []
    ctx_optional_inputs = {}
    for inp in input_list:
        data = _all_context_input_output_data[inp]
        list_ctx_return_types.append(data[1])
        list_ctx_return_names.append(data[2])
        # Add tooltips for UI clarity
        tooltip = f"Optional input for '{data[0]}'. Accepts type: {data[1]}."
        ctx_optional_inputs[data[0]] = tuple(
            [data[1], {"forceInput": True, "tooltip": tooltip}] if data[1] in force_input_types or data[0] in force_input_names else [data[1], {"tooltip": tooltip}]
        )
    ctx_return_types = tuple(list_ctx_return_types)
    ctx_return_names = tuple(list_ctx_return_names)
    return (ctx_optional_inputs, ctx_optional_inputs, ctx_return_types, ctx_return_names)  # inputs and outputs

ALL_CTX_OPTIONAL_INPUTS, ALL_CTX_OPTIONAL_OUTPUTS, ALL_CTX_RETURN_TYPES, ALL_CTX_RETURN_NAMES = _create_context_data()

def new_context(pipe=None, **kwargs):
    # Creates a new context from the provided data, with an optional base ctx to start.
    # pipe can be dict or tuple
    if isinstance(pipe, tuple):
        # Assume it's the tuple from get_context_return_tuple, first is dict
        context = pipe[0] if pipe else {}
    elif isinstance(pipe, dict):
        context = pipe
    else:
        context = {}
    # Only copy known keys from pipe input, ignore unknown keys
    new_ctx = {}
    for key in _all_context_input_output_data:
        if key == "pipe":
            continue
        if key in context:
            new_ctx[key] = context[key]
    # Apply kwargs overrides for known keys
    for key in _all_context_input_output_data:
        if key == "pipe":
            continue
        v = kwargs.get(key, None)
        if v is not None:
            new_ctx[key] = v
    return new_ctx

def get_context_return_tuple(ctx, inputs_list=None):
    # Returns a tuple for returning in the order of the inputs list.
    if inputs_list is None:
        inputs_list = _all_context_input_output_data.keys()
    tup_list = [ctx]
    for key in inputs_list:
        if key == "pipe":
            continue
        tup_list.append(ctx.get(key, None))
    return tuple(tup_list)

class RvPipe_IO_Context_Video:
    # Node class for passing through a context for general workflows.
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": ALL_CTX_OPTIONAL_INPUTS,
            "hidden": {},
        }

    RETURN_TYPES = ALL_CTX_RETURN_TYPES
    RETURN_NAMES = ALL_CTX_RETURN_NAMES
    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PIPE.value
    FUNCTION = "execute"

    def execute(self, pipe=None, **kwargs):
        # Read the pipe input (dict or tuple), update with connected inputs
        ctx = new_context(pipe, **kwargs)
        # Return the updated pipe and all individual values
        return get_context_return_tuple(ctx)

NODE_NAME = 'Context Video [RvTools-X]'
NODE_DESC = 'Context Video'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvPipe_IO_Context_Video
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}