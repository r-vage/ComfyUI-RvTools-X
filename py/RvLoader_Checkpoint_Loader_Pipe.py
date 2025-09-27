# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import os
import comfy
import comfy.sd
import torch
import folder_paths

from ..core import CATEGORY, cstr
from ..core.common import RESOLUTION_PRESETS, RESOLUTION_MAP

MAX_RESOLUTION = 32768

# Latent / UNet downsample info
LATENT_CHANNELS = 4
UNET_DOWNSAMPLE = 8

def _detect_latent_channels_from_vae_obj(vae_obj) -> int:
#     Try to infer latent channel count from a VAE-like object. Return default on failure.
    try:
        if hasattr(vae_obj, 'channels') and isinstance(getattr(vae_obj, 'channels'), int):
            return getattr(vae_obj, 'channels')
        if hasattr(vae_obj, 'latent_channels') and isinstance(getattr(vae_obj, 'latent_channels'), int):
            return getattr(vae_obj, 'latent_channels')
        for attr in ('encoder', 'conv_in', 'down_blocks'):
            sub = getattr(vae_obj, attr, None)
            if sub is not None and hasattr(sub, 'weight'):
                w = getattr(sub, 'weight')
                try:
                    if hasattr(w, 'ndim') and w.ndim == 4:
                        return int(w.shape[0])
                except Exception:
                    pass
    except Exception:
        pass
    return LATENT_CHANNELS

class RvLoader_Checkpoint_Loader_Pipe:
    resolution = RESOLUTION_PRESETS
    resolution_map = RESOLUTION_MAP

    def __init__(self) -> None:
        pass

    @classmethod
    def INPUT_TYPES(cls) -> dict:
        return {
            "required": {
                "ckpt_name": (folder_paths.get_filename_list("checkpoints"), "Select a checkpoint file to load. Prefer .safetensors for safety"),
                "vae_name": (["Baked VAE"] + folder_paths.get_filename_list("vae"), "Optional VAE to load (or use baked VAE in the checkpoint)"),
                "Baked_Clip": ("BOOLEAN", {"default": True}, "If enabled, return the baked CLIP from the checkpoint"),
                "Use_Clip_Layer": ("BOOLEAN", {"default": True}, "If enabled, trim CLIP to the requested layer index"),
                "stop_at_clip_layer": ("INT", {"default": -2, "min": -24, "max": -1, "step": 1}, "When trimming CLIP, stop at this layer index"),
                "resolution": (cls.resolution, "Preset resolution; choose Custom to use width/height"),
                "width": ("INT", {"default": 512, "min": 16, "max": MAX_RESOLUTION, "step": 8}, "Pixel width when resolution is Custom"),
                "height": ("INT", {"default": 512, "min": 16, "max": MAX_RESOLUTION, "step": 8}, "Pixel height when resolution is Custom"),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 4096}, "Batch size for latent tensor"),
            },
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.CHECKPOINT.value

    RETURN_TYPES = ("pipe",)
    FUNCTION = "execute"

    def execute(
        self,
        ckpt_name: str,
        vae_name: str,
        Baked_Clip: bool,
        Use_Clip_Layer: bool,
        stop_at_clip_layer: int,
        batch_size: int,
        resolution: str,
        width: int,
        height: int,
    ) -> tuple:
        # Type assertions (enforced by type hints, but keep for runtime safety)
        if not isinstance(ckpt_name, str):
            raise TypeError("ckpt_name must be a string")
        if not isinstance(vae_name, str):
            raise TypeError("vae_name must be a string")
        if not isinstance(Baked_Clip, bool):
            Baked_Clip = bool(Baked_Clip)
        if not isinstance(Use_Clip_Layer, bool):
            Use_Clip_Layer = bool(Use_Clip_Layer)

        # Resolve checkpoint path and perform light validations
        ckpt_path: str = folder_paths.get_full_path("checkpoints", ckpt_name)
        safe_exts: set[str] = {".safetensors", ".sft"}
        legacy_exts: set[str] = {".ckpt", ".pt", ".pth"}

        # Check extension and emit warnings where appropriate
        _, ext = os.path.splitext(ckpt_path.lower())
        if ext in legacy_exts:
            cstr(f"Selected checkpoint '{ckpt_name}' uses legacy extension '{ext}'. Consider converting to .safetensors for better safety/performance.").msg.print()

        # Existence and access checks
        if not os.path.isfile(ckpt_path):
            raise RuntimeError(f"Checkpoint path not found: {ckpt_path}")
        if not os.access(ckpt_path, os.R_OK):
            raise RuntimeError(f"Checkpoint file is not readable: {ckpt_path}")

        output_vae: bool = (vae_name == "Baked VAE")

        loaded_ckpt = comfy.sd.load_checkpoint_guess_config(
            ckpt_path,
            output_vae=output_vae,
            output_clip=Baked_Clip,
            embedding_directory=folder_paths.get_folder_paths("embeddings"),
        )

        vae_path: str = ""
        loaded_vae = None
        if vae_name == "Baked VAE":
            # Cache commonly used checkpoint parts defensively and avoid multiple slices
            ckpt_parts = loaded_ckpt[:3] if hasattr(loaded_ckpt, '__len__') and len(loaded_ckpt) >= 3 else None
            loaded_vae = ckpt_parts[2] if ckpt_parts is not None else None
        else:
            vae_path = folder_paths.get_full_path("vae", vae_name)
            if not os.path.isfile(vae_path):
                cstr(f"Selected VAE not found: {vae_path}. Falling back to baked VAE if available.").msg.print()
                # use cached parts if available
                loaded_vae = ckpt_parts[2] if 'ckpt_parts' in locals() and ckpt_parts is not None else (loaded_ckpt[:3][2] if len(loaded_ckpt) >= 3 else None)
            else:
                loaded_vae = comfy.sd.VAE(sd=comfy.utils.load_torch_file(vae_path))

        # Only clone CLIP when we actually intend to modify/trim it. Avoiding an unconditional clone saves memory/time for large models.
        loaded_clip = None
        # Use cached ckpt_parts when possible to avoid repeated slicing
        if 'ckpt_parts' not in locals():
            ckpt_parts = loaded_ckpt[:3] if hasattr(loaded_ckpt, '__len__') and len(loaded_ckpt) >= 3 else None
        if Baked_Clip and ckpt_parts is not None:
            base_clip = ckpt_parts[1]
            if Use_Clip_Layer:
                loaded_clip = base_clip.clone()
                loaded_clip.clip_layer(stop_at_clip_layer)
            else:
                loaded_clip = base_clip

        # Map preset resolution -> width/height efficiently
        if resolution != "Custom" and resolution in self.resolution_map:
            width, height = self.resolution_map[resolution]

        # Detect latent channels from external VAE or baked VAE when available
        detected_latent_channels = LATENT_CHANNELS
        try:
            if vae_name != "Baked VAE":
                vae_path = folder_paths.get_full_path("vae", vae_name)
                if vae_path and os.path.isfile(vae_path):
                    sd_obj = comfy.utils.load_torch_file(vae_path)
                    try:
                        vae_inst = comfy.sd.VAE(sd=sd_obj)
                        detected_latent_channels = _detect_latent_channels_from_vae_obj(vae_inst)
                        cstr(f"Detected Latent Channels: {detected_latent_channels}").msg.print()
                    except Exception:
                        if isinstance(sd_obj, dict):
                            for k, v in sd_obj.items():
                                if hasattr(v, 'ndim') and v.ndim == 4:
                                    detected_latent_channels = int(v.shape[0])
                                    cstr(f"Detected Latent Channels: {detected_latent_channels}").warning.print()
                                    break
            else:
                if 'ckpt_parts' in locals() and ckpt_parts is not None and len(ckpt_parts) >= 3 and ckpt_parts[2] is not None:
                    detected_latent_channels = _detect_latent_channels_from_vae_obj(ckpt_parts[2])
                    cstr(f"Detected Latent Channels: {detected_latent_channels}").msg.print()
        except Exception:
            detected_latent_channels = LATENT_CHANNELS
            cstr(f"Fallback to Default Latent Channels: {detected_latent_channels}").warning.print()

        latent = torch.zeros([batch_size, detected_latent_channels, height // UNET_DOWNSAMPLE, width // UNET_DOWNSAMPLE])

        # Compose result list efficiently and defensively
        model_obj = ckpt_parts[0] if 'ckpt_parts' in locals() and ckpt_parts is not None and len(ckpt_parts) >= 1 else (loaded_ckpt if loaded_ckpt is not None else None)
        pipe = {
            "model": model_obj,
            "clip": loaded_clip,
            "vae": loaded_vae,
            "latent": {"samples": latent},
            "width": int(width),
            "height": int(height),
            "batch_size": int(batch_size),
            "model_name": str(ckpt_name),
            "vae_name": "" if vae_name == "Baked VAE" else str(vae_name),
            "clip_skip": int(stop_at_clip_layer),
        }

        return (pipe,)

NODE_NAME = "Checkpoint Loader (Pipe) [RvTools-X]"
NODE_DESC = "Checkpoint Loader (Pipe)"

NODE_CLASS_MAPPINGS = {NODE_NAME: RvLoader_Checkpoint_Loader_Pipe}

NODE_DISPLAY_NAME_MAPPINGS = {NODE_NAME: NODE_DESC}