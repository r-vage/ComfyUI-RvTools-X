# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import os
import comfy
import comfy.sd
import torch
import folder_paths

from ..core import CATEGORY, cstr, RESOLUTION_PRESETS, RESOLUTION_MAP

MAX_RESOLUTION = 32768

# Latent / UNet downsample defaults
LATENT_CHANNELS = 4
UNET_DOWNSAMPLE = 8

def _detect_latent_channels_from_vae_obj(vae_obj) -> int:
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

class RvLoader_Checkpoint_Loader:
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

    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "LATENT", "STRING")
    RETURN_NAMES = ("model", "clip", "vae", "latent", "model_name")
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
        # Minimal type assertions (assume UI provides correct types)
        ckpt_path = folder_paths.get_full_path("checkpoints", ckpt_name)
        legacy_exts = {".ckpt", ".pt", ".pth"}
        _, ext = os.path.splitext(ckpt_path.lower())
        if ext in legacy_exts:
            cstr(f"Selected checkpoint '{ckpt_name}' uses legacy extension '{ext}'. Consider converting to .safetensors for better safety/performance.").warning.print()
        if not os.path.isfile(ckpt_path):
            msg = f"Checkpoint path not found: {ckpt_path}"
            cstr(msg).error.print()
            raise RuntimeError(msg)
        if not os.access(ckpt_path, os.R_OK):
            msg = f"Checkpoint file is not readable: {ckpt_path}"
            cstr(msg).error.print()
            raise RuntimeError(msg)

        output_vae = (vae_name == "Baked VAE")
        loaded_ckpt = comfy.sd.load_checkpoint_guess_config(
            ckpt_path,
            output_vae=output_vae,
            output_clip=Baked_Clip,
            embedding_directory=folder_paths.get_folder_paths("embeddings"),
        )
        # Cache tuple slice for performance
        ckpt_model, ckpt_clip, ckpt_vae = loaded_ckpt[:3]

        # VAE selection
        if vae_name == "Baked VAE":
            loaded_vae = ckpt_vae
        else:
            vae_path = folder_paths.get_full_path("vae", vae_name)
            if not os.path.isfile(vae_path):
                cstr(f"Selected VAE not found: {vae_path}. Falling back to baked VAE if available.").warning.print()
                loaded_vae = ckpt_vae
            else:
                loaded_vae = comfy.sd.VAE(sd=comfy.utils.load_torch_file(vae_path))

        # CLIP selection
        if Baked_Clip:
            if Use_Clip_Layer:
                loaded_clip = ckpt_clip.clone()
                loaded_clip.clip_layer(stop_at_clip_layer)
            else:
                loaded_clip = ckpt_clip
        else:
            loaded_clip = None

        # Efficient resolution mapping
        if resolution != "Custom" and resolution in self.resolution_map:
            width, height = self.resolution_map[resolution]

        # Attempt detection of latent channels from external or baked VAE
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
                # baked VAE from checkpoint (if available)
                if 'ckpt_vae' in locals() and ckpt_vae is not None:
                    detected_latent_channels = _detect_latent_channels_from_vae_obj(ckpt_vae)
                    cstr(f"Detected Latent Channels: {detected_latent_channels}").msg.print()
        except Exception:
            detected_latent_channels = LATENT_CHANNELS
            cstr(f"Fallback to Default Latent Channels: {detected_latent_channels}").warning.print()

        latent = torch.zeros([batch_size, detected_latent_channels, height // UNET_DOWNSAMPLE, width // UNET_DOWNSAMPLE])
        return (ckpt_model, loaded_clip, loaded_vae, {"samples": latent}, ckpt_name)

NODE_NAME = "Checkpoint Loader [RvTools-X]"
NODE_DESC = "Checkpoint Loader"

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvLoader_Checkpoint_Loader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
