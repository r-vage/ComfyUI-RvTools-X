# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from ..core import CATEGORY, AnyType

any = AnyType("*")

class RvPipe_Out_Sampler_Settings:
    #Unified pipe-out node that extracts sampler/scheduler/settings from a pipe.
    #
    # The pipe formats in the repo vary (Simple, Small, Flux, DualScheduler, etc.).
    # This node attempts to read values from the pipe by position and will supply
    # safe defaults for any missing elements so all outputs are always present.

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pipe": ("pipe", {"tooltip": "Input pipe containing sampler settings produced by rvsettings_sampler_settings* nodes."}),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PIPE.value
    # Combined return types: pipe + many optional fields (use `any` for complex objects)
    RETURN_TYPES = (
        any,  # sampler
        any,  # scheduler
        "INT",  # steps
        "FLOAT",  # cfg
        "FLOAT",  # guidance
        "FLOAT",  # denoise
        "FLOAT",  # sigmas_denoise
        "FLOAT",  # noise_strength
        "INT",    # seed
    )

    RETURN_NAMES = (
        "sampler",
        "scheduler",
        "steps",
        "cfg",
        "guidance",
        "denoise",
        "sigmas_denoise",
        "noise_strength",
        "seed",
    )

    FUNCTION = "execute"

    def execute(self, pipe: tuple = None) -> tuple:
        # Unpack a variety of sampler-settings pipe shapes and return a full set
        # of outputs. Missing entries are replaced with sensible defaults.
        
        if pipe is None:
            raise ValueError("Input pipe is required for Pipe Out Sampler Settings.")

        # Prefer dict-style pipes. If provided a dict, map canonical keys into a
        # positional sequence so existing heuristics still function. If provided an
        # iterable, coerce to list and operate as before.
        if isinstance(pipe, dict):
            seq = [
                pipe.get("sampler", None),
                pipe.get("scheduler", None),
                pipe.get("steps", None),
                pipe.get("cfg", None),
                pipe.get("guidance", None),
                pipe.get("denoise", None),
                pipe.get("sigmas_denoise", None),
                pipe.get("noise_strength", None),
                pipe.get("seed", None),
            ]
        else:
            try:
                seq = list(pipe)
            except Exception:
                raise ValueError("Input pipe must be a dict with named fields or an iterable (tuple/list) produced by an rvsettings_sampler_settings* node.")

        # Helper to safely grab value at index or return default
        def _get(i, default=None):
            return seq[i] if 0 <= i < len(seq) else default

        # Provide explicit sensible defaults for each expected field. The original
        # pipe variants vary in length/ordering; choose defaults that are safe for
        # downstream nodes rather than raising when values are missing.
        sampler = _get(0, None)
        scheduler = _get(1, None)

        # New normalized layout: many of the simplified "pipe out" nodes place
        # numeric settings starting at index 2 (steps) or 3; we'll use a small
        # heuristic: prefer index 2 for steps if it's numeric-like, otherwise
        # fall back to index 3. This keeps compatibility with older shapes.
        def _to_int(val, default=0):
            try:
                return int(val)
            except Exception:
                return default

        def _to_float(val, default=0.0):
            try:
                return float(val)
            except Exception:
                return default

        # Common positions (covers most variants). Use heuristic to detect
        # whether steps live at index 2 or 3.
        raw_steps_idx = 2 if isinstance(_get(2, None), (int, float, str)) else 3
        steps = _to_int(_get(raw_steps_idx, None), 0)
        cfg = _to_float(_get(raw_steps_idx + 1, None), 0.0)
        guidance = _to_float(_get(raw_steps_idx + 2, None), 0.0)
        denoise = _to_float(_get(raw_steps_idx + 3, None), 0.0)
        sigmas_denoise = _to_float(_get(raw_steps_idx + 4, None), 0.0)
        noise_strength = _to_float(_get(raw_steps_idx + 5, None), 0.0)

        # Seed placement varies between pipe variants. Common positions:
        # - Flux+Seed nodes often put seed at index 6 (zero-based)
        # - Longer variants may put seed at raw_steps_idx + 6
        # Try a small set of likely indices and coerce numeric-like values.
        seed = None
        candidate_indices = []
        # Prefer explicit index 6 (many Flux variants)
        candidate_indices.append(6)
        # Then the position relative to detected steps index
        candidate_indices.append(raw_steps_idx + 6)
        # Finally try the last element
        candidate_indices.append(len(seq) - 1)

        seen = set()
        for idx in candidate_indices:
            if idx in seen:
                continue
            seen.add(idx)
            val = _get(idx, None)
            if val is None:
                continue
            # Accept ints directly or numeric strings
            if isinstance(val, int):
                seed = val
                break
            if isinstance(val, str):
                s = val.strip()
                if s.isdigit():
                    seed = int(s)
                    break
                # allow float-like strings that are integers
                try:
                    f = float(s)
                except Exception:
                    continue
                if abs(f - int(f)) < 1e-9:
                    seed = int(f)
                    break
            # If it's a float, only accept it when it's integer-like
            if isinstance(val, float):
                if abs(val - int(val)) < 1e-9:
                    seed = int(val)
                    break
                else:
                    # not an integer-valued float - skip
                    continue
            # As a last resort, try coercion for other types that may represent integers
            try:
                iv = int(val)
            except Exception:
                continue
            else:
                seed = iv
                break

        if seed is None:
            seed = 0

        # Final normalization/coercion
        steps = _to_int(steps, 0)
        cfg = _to_float(cfg, 0.0)
        guidance = _to_float(guidance, 0.0)
        denoise = _to_float(denoise, 0.0)
        sigmas_denoise = _to_float(sigmas_denoise, 0.0)
        noise_strength = _to_float(noise_strength, 0.0)
        seed = _to_int(seed, 0)

        return (
            sampler,
            scheduler,
            steps,
            cfg,
            guidance,
            denoise,
            sigmas_denoise,
            noise_strength,
            seed,
        )


NODE_NAME = 'Pipe Out Sampler Settings [RvTools-X]'
NODE_DESC = 'Pipe Out Sampler Settings'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvPipe_Out_Sampler_Settings
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
