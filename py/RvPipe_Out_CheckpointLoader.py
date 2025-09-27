# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY

UNET_DOWNSAMPLE = 8

class RvPipe_Out_CheckpointLoader:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pipe": ("pipe", {"tooltip": "Input pipe containing model, clip, vae, latent, width, height, batch size, and names."}),
            },
            "optional": {
                "latent": ("LATENT", {"tooltip": "Optional latent input to use if pipe does not supply latent, width, or height."}),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PIPE.value
    # Backwards-compatible: older pipes have 9 elements; newer pipes may include an
    # additional `clip_skip` (stop_at_clip_layer) integer at position 10.
    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "LATENT", "INT", "INT", "INT", "STRING", "STRING", "INT")
    RETURN_NAMES = ("model", "clip", "vae", "latent", "width", "height", "batch_size", "model_name", "vae_name", "clip_skip")
    FUNCTION = "execute"

    def execute(self, pipe: dict = None, latent: dict = None) -> tuple:
        # Expect dict-style pipe. Tuples have been deprecated for pipe interchange.
        if pipe is None:
            raise ValueError("Input pipe must not be None and must be a dict-style pipe")
        if not isinstance(pipe, dict):
            raise ValueError("RvPipe_Out_CheckpointLoader expects dict-style pipes only.")

        # Prefer object fields; fall back to name fields only where appropriate.
        model = pipe.get("model")
        clip = pipe.get("clip")
        vae = pipe.get("vae")
        latent_from_pipe = pipe.get("latent")

        # Numeric fields and batch size
        width = pipe.get("width")
        height = pipe.get("height")
        batch_size = pipe.get("batch_size")

        # Coerce simple numeric types where appropriate
        try:
            if width is not None:
                width = int(width)
        except Exception:
            width = None
        try:
            if height is not None:
                height = int(height)
        except Exception:
            height = None
        try:
            if batch_size is not None:
                batch_size = int(batch_size)
        except Exception:
            batch_size = None

        # If pipe has no width/height and latent input is provided, derive from latent shape
        if (width is None or height is None) and latent is not None:
            latent_shape = latent["samples"].shape
            if height is None:
                height = latent_shape[2] * UNET_DOWNSAMPLE
            if width is None:
                width = latent_shape[3] * UNET_DOWNSAMPLE

        # Use latent from pipe if it has valid samples, otherwise fallback to input latent
        if latent_from_pipe is not None and latent_from_pipe.get("samples") is not None:
            output_latent = latent_from_pipe
        else:
            output_latent = latent

        # Name fields (textual)
        model_name = pipe.get("model_name")
        vae_name = pipe.get("vae_name")
        clip_skip = pipe.get("clip_skip")

        return (model, clip, vae, output_latent, width, height, batch_size, model_name, vae_name, clip_skip)

NODE_NAME = 'Pipe Out Checkpoint Loader [RvTools-X]'
NODE_DESC = 'Pipe Out Checkpoint Loader'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvPipe_Out_CheckpointLoader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}