# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import time
from server import PromptServer
from ..core import CATEGORY
from ..core import AnyType

# Credits to LAOGOU-666: https://github.com/LAOGOU-666/Comfyui-Memory_Cleanup.git
# Class and mapping renamed to avoid conflicts with the original node
# improved and adapted for ComfyUI-RvTools-X
any = AnyType("*")

class Rv_Settings_VRAMCleanup:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "anything": (any, {}),
                "offload_model": ("BOOLEAN", {"default": True, "label": "Offload Models"}),
                "offload_cache": ("BOOLEAN", {"default": True, "label": "Clear VRAM Cache"}),
            },
            "optional": {},
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            }
        }

    RETURN_TYPES = (any,)
    RETURN_NAMES = ("output",)
    OUTPUT_NODE = True
    FUNCTION = "empty_cache"
    CATEGORY = CATEGORY.MAIN.value + CATEGORY.SETTINGS.value

    def _validate_prompt_server(self):
        """Validate that PromptServer is available and accessible"""
        try:
            if not hasattr(PromptServer, 'instance') or PromptServer.instance is None:
                return False, "PromptServer instance not available"
            return True, None
        except Exception as e:
            return False, f"PromptServer validation error: {e}"

    def _send_cleanup_signal(self, offload_model, offload_cache):
        """Send cleanup signal to ComfyUI frontend"""
        signal_data = {
            "type": "cleanup_request",
            "data": {
                "unload_models": bool(offload_model),
                "free_memory": bool(offload_cache)
            }
        }

        try:
            PromptServer.instance.send_sync("memory_cleanup", signal_data)
            return True, signal_data
        except AttributeError as e:
            return False, f"PromptServer method not available: {e}"
        except Exception as e:
            return False, f"Failed to send cleanup signal: {e}"

    def empty_cache(self, anything, offload_model, offload_cache, unique_id=None, extra_pnginfo=None):
        """Send VRAM cleanup signal to ComfyUI frontend with validation and feedback"""
        start_time = time.time()

        try:
            # Validate inputs
            if not isinstance(offload_model, bool):
                offload_model = bool(offload_model)
            if not isinstance(offload_cache, bool):
                offload_cache = bool(offload_cache)

            print(f"VRAM Cleanup - Models: {'OFFLOAD' if offload_model else 'KEEP'}, "
                  f"Cache: {'CLEAR' if offload_cache else 'KEEP'}")

            # Validate PromptServer availability
            server_ok, server_error = self._validate_prompt_server()
            if not server_ok:
                print(f"Error: {server_error}")
                print("VRAM cleanup requires ComfyUI frontend to be running")
                return (anything,)

            # Send cleanup signal
            signal_sent, signal_result = self._send_cleanup_signal(offload_model, offload_cache)

            if signal_sent:
                signal_data = signal_result
                print("VRAM cleanup signal sent successfully")
                print(f"Signal details: Unload models={signal_data['data']['unload_models']}, "
                      f"Free memory={signal_data['data']['free_memory']}")

                # Brief pause to allow frontend processing
                time.sleep(0.5)

                elapsed = time.time() - start_time
                print(f"VRAM cleanup completed in {elapsed:.2f} seconds")

            else:
                print(f"Failed to send VRAM cleanup signal: {signal_result}")
                print("The ComfyUI frontend may not support memory cleanup operations")

        except Exception as e:
            elapsed = time.time() - start_time
            print(f"Critical error during VRAM cleanup after {elapsed:.2f} seconds: {e}")
            import traceback
            traceback.print_exc()

        return (anything,)


NODE_NAME = 'VRAM Cleanup [RvTools-X]'
NODE_DESC = 'VRAM Cleanup'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: Rv_Settings_VRAMCleanup
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}