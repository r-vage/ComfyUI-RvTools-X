# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import os
import comfy
import comfy.sd
import torch
import folder_paths
import comfy.utils

from ..core import CATEGORY, cstr

class RvLoader_Checkpoint_Loader_v3_Pipe:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "ckpt_name": (folder_paths.get_filename_list("checkpoints") + ["None"], {"default": "None"}, "Checkpoint filename to load (or 'None' to use a UNet file)"),
                "unet_name": (folder_paths.get_filename_list("diffusion_models") + ["None"], {"default": "None"}, "Diffusion UNet checkpoint (used when 'load_unet_checkpoint' is True)"),
                "weight_dtype": (["default", "fp8_e4m3fn", "fp8_e4m3fn_fast", "fp8_e5m2"], {"default": "default"}, "Weight dtype for UNet when loading a diffusion model"),
                "clip_name1": (folder_paths.get_filename_list("clip") + ["None"], {"default": "None"}, "Primary CLIP module (or 'None' to use baked CLIP from the checkpoint)"),
                "clip_name2": (folder_paths.get_filename_list("clip") + ["None"], {"default": "None"}, "Optional second CLIP module (for ensemble)"),
                "clip_name3": (folder_paths.get_filename_list("clip") + ["None"], {"default": "None"}, "Optional third CLIP module (for ensemble)"),
                "clip_type_": (["sdxl", "sd3", "flux", "qwen_image", "hidream", "hunyuan_image", "wan"], {"default": "flux"}, "CLIP flavor/type to interpret when loading external CLIP modules"),
                "vae_name": (["Baked VAE"] + folder_paths.get_filename_list("vae"), {"default": "Baked VAE"}, "VAE file to load, or use baked VAE from the checkpoint"),
                "baked_clip": ("BOOLEAN", {"default": True}, "Use baked CLIP from checkpoint if available"),
                "enable_clip_layer": ("BOOLEAN", {"default": True}, "When enabled, trim CLIP to `stop_at_clip_layer` (memory-costly)"),
                "stop_at_clip_layer": ("INT", {"default": -2, "min": -24, "max": -1, "step": 1}, "Layer index to stop at when trimming CLIP"),
                "load_unet_checkpoint": ("BOOLEAN", {"default": False}, "If True, load a UNet checkpoint from 'unet_name' instead of a regular checkpoint"),
            },
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.CHECKPOINT.value

    RETURN_TYPES = ("pipe",)
    FUNCTION = "execute"

    def execute(self, ckpt_name: str, unet_name: str, weight_dtype: str, clip_name1: str, clip_name2: str, clip_name3: str, clip_type_: str,
                vae_name: str, baked_clip: bool, enable_clip_layer: bool, stop_at_clip_layer: int, load_unet_checkpoint: bool) -> tuple:

        # normalize boolean-ish inputs
        baked_clip = bool(baked_clip)
        enable_clip_layer = bool(enable_clip_layer)
        load_unet_checkpoint = bool(load_unet_checkpoint)

        # Defensive: some graphs (or older backups) may accidentally wire a boolean
        # into the `vae_name` input. Normalize that to safe string values so the
        # node validation doesn't fail later. True -> 'Baked VAE', False -> 'None'.
        if isinstance(vae_name, bool):
            if vae_name:
                cstr("vae_name received boolean True; coercing to 'Baked VAE'").msg.print()
                vae_name = "Baked VAE"
            else:
                cstr("vae_name received boolean False; coercing to 'None'").msg.print()
                vae_name = "None"

        checkpoint = ""
        vae_path = ""
        clip_path1 = ""
        clip_path2 = ""
        clip_path3 = ""
        loaded_clip = None
        ckpt_parts = None

        baked_vae = (vae_name == "Baked VAE")

        # simple presence check
        if (ckpt_name in (None, '', 'undefined', 'None')) and (unet_name in (None, '', 'undefined', 'None')):
            raise ValueError("Missing Input: No Checkpoint selected")

        safe_exts = {".safetensors", ".sft"}

        # Regular checkpoint path
        if ckpt_name not in (None, '', 'undefined', 'None') and not load_unet_checkpoint:
            ckpt_path = folder_paths.get_full_path("checkpoints", ckpt_name)

            # extension and existence checks
            _, ext = os.path.splitext(ckpt_path.lower())
            # Prefers safetensors; warn if extension is not a known safe extension
            if ext not in safe_exts:
                cstr(f"Selected checkpoint '{ckpt_name}' uses non-preferred extension '{ext}'. Consider converting to .safetensors for safety/performance.").msg.print()

            # Ensure the checkpoint path exists and is readable. Fail-fast when
            # the file cannot be accessed rather than silently logging and
            # letting a downstream loader raise a less-helpful error.
            if not os.path.isfile(ckpt_path) or not os.access(ckpt_path, os.R_OK):
                msg = f"Checkpoint file not found or not readable: {ckpt_path}"
                cstr(msg).error.print()
                raise RuntimeError(msg)

            # load the checkpoint (may include baked VAE/CLIP)
            loaded_ckpt = comfy.sd.load_checkpoint_guess_config(
                ckpt_path,
                output_vae=baked_vae,
                output_clip=baked_clip,
                embedding_directory=folder_paths.get_folder_paths("embeddings"),
            )
            checkpoint = ckpt_name
            # Cache commonly used checkpoint parts defensively
            ckpt_parts = loaded_ckpt[:3] if hasattr(loaded_ckpt, '__len__') and len(loaded_ckpt) >= 3 else None
            # handle baked clip (clone only when trimming requested)
            if baked_clip and ckpt_parts is not None:
                base_clip = ckpt_parts[1]
                if enable_clip_layer:
                    loaded_clip = base_clip.clone()
                    loaded_clip.clip_layer(stop_at_clip_layer)
                else:
                    loaded_clip = base_clip

        # UNet checkpoint
        elif unet_name not in (None, '', 'undefined', 'None') and load_unet_checkpoint:
            model_options = {}
            if weight_dtype == "fp8_e4m3fn":
                model_options["dtype"] = torch.float8_e4m3fn
            elif weight_dtype == "fp8_e4m3fn_fast":
                model_options["dtype"] = torch.float8_e4m3fn
                model_options["fp8_optimizations"] = True
            elif weight_dtype == "fp8_e5m2":
                model_options["dtype"] = torch.float8_e5m2

            ckpt_path = folder_paths.get_full_path_or_raise("diffusion_models", unet_name)
            _, ext = os.path.splitext(ckpt_path.lower())
            if ext not in safe_exts:
                cstr(f"Selected UNet checkpoint '{unet_name}' uses non-preferred extension '{ext}'. Consider converting to .safetensors.").msg.print()

            # Verify UNet checkpoint accessibility and fail-fast on error.
            if not os.path.isfile(ckpt_path) or not os.access(ckpt_path, os.R_OK):
                msg = f"UNet checkpoint not found or not readable: {ckpt_path}"
                cstr(msg).error.print()
                raise RuntimeError(msg)

            loaded_ckpt = comfy.sd.load_diffusion_model(ckpt_path, model_options=model_options)
            checkpoint = unet_name

        else:
            raise ValueError("Missing Input: No Checkpoint selected or wrong combination of settings.")

        # VAE loading
        if vae_name == "Baked VAE":
            if not load_unet_checkpoint:
                loaded_vae = ckpt_parts[2] if ckpt_parts is not None else None
            else:
                raise ValueError("Missing Input: Select a VAE File when loading a UNet checkpoint")
        else:
            vae_path = folder_paths.get_full_path("vae", vae_name)
            if not os.path.isfile(vae_path):
                cstr(f"Selected VAE not found: {vae_path}. Falling back to baked VAE if available.").msg.print()
                loaded_vae = ckpt_parts[2] if ckpt_parts is not None else None
            else:
                loaded_vae = comfy.sd.VAE(sd=comfy.utils.load_torch_file(vae_path))

        # CLIP mapping
        if clip_type_ == "sdxl":
            clip_type = comfy.sd.CLIPType.STABLE_DIFFUSION
        elif clip_type_ == "sd3":
            clip_type = comfy.sd.CLIPType.SD3
        elif clip_type_ == "flux":
            clip_type = comfy.sd.CLIPType.FLUX
        elif clip_type_ == "qwen_image":
            clip_type = comfy.sd.CLIPType.QWEN_IMAGE
        elif clip_type_ == "hidream":
            clip_type = comfy.sd.CLIPType.HIDREAM
        elif clip_type_ == "hunyuan_image":
            clip_type = comfy.sd.CLIPType.HUNYUAN_IMAGE
        elif clip_type_ == "chroma":
            clip_type = comfy.sd.CLIPType.CHROMA
        elif clip_type_ == "wan":
            clip_type = comfy.sd.CLIPType.WAN
        else:
            clip_type = comfy.sd.CLIPType.STABLE_DIFFUSION

        # load external CLIP modules when baked_clip is False
        if not baked_clip:
            if clip_name1 not in (None, '', 'undefined', 'None'):
                clip_path1 = folder_paths.get_full_path_or_raise("clip", clip_name1)
            else:
                raise ValueError("Missing Input: Select a Clip Model for 'clip_name1' or set 'baked_clip' = True")

            if clip_name2 not in (None, '', 'undefined', 'None'):
                clip_path2 = folder_paths.get_full_path_or_raise("clip", clip_name2)

            if clip_name3 not in (None, '', 'undefined', 'None'):
                clip_path3 = folder_paths.get_full_path_or_raise("clip", clip_name3)

            ckpt_list = [p for p in (clip_path1, clip_path2, clip_path3) if p]
            if ckpt_list:
                loaded_clip = comfy.sd.load_clip(
                    ckpt_paths=ckpt_list,
                    embedding_directory=folder_paths.get_folder_paths("embeddings"),
                    clip_type=clip_type,
                )
        else:
            if load_unet_checkpoint:
                raise ValueError("Missing Input: CLIP, set 'baked_clip' to False and select clip models when loading a UNet checkpoint.")

        if loaded_clip is None:
            raise ValueError("Missing Input: CLIP")

        # Normalize into canonical dict-style pipe
        pipe = {
            "model": loaded_ckpt if load_unet_checkpoint else (ckpt_parts[0] if ckpt_parts is not None else loaded_ckpt),
            "clip": loaded_clip,
            "vae": loaded_vae,
            "latent": {"samples": None},
            "width": None,
            "height": None,
            "batch_size": int(1),
            "model_name": checkpoint,
            "vae_name": '' if vae_name == "Baked VAE" else str(vae_name),
            "clip_skip": int(stop_at_clip_layer),
        }
        return (pipe,)

NODE_NAME = 'Checkpoint Loader v3 (Pipe) [RvTools-X]'
NODE_DESC = 'Checkpoint Loader v3 (Pipe)'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvLoader_Checkpoint_Loader_v3_Pipe
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}