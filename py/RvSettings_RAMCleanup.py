# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import psutil
import ctypes
from ctypes import wintypes
import time
import platform
import subprocess
from server import PromptServer
from ..core import CATEGORY
from ..core import AnyType

# Credits to LAOGOU-666: https://github.com/LAOGOU-666/Comfyui-Memory_Cleanup.git
# Class and mapping renamed to avoid conflicts with the original node
# improved and adapted for ComfyUI-RvTools-X

any = AnyType("*")

class RvSettings_RAMCleanup:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "anything": (any, {}),
                "clean_file_cache": ("BOOLEAN", {"default": True, "label": "Clear File Cache"}),
                "clean_processes": ("BOOLEAN", {"default": True, "label": "Clear Process Memory"}),
                "clean_dlls": ("BOOLEAN", {"default": True, "label": "Clear Unused DLLs"}),
                "retry_times": ("INT", {
                    "default": 3,
                    "min": 1,
                    "max": 10,
                    "step": 1,
                    "label": "Retry Times"
                }),
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
    FUNCTION = "clean_ram"
    CATEGORY = CATEGORY.MAIN.value + CATEGORY.SETTINGS.value

    def get_ram_usage(self):
        """Get current RAM usage statistics"""
        memory = psutil.virtual_memory()
        return memory.percent, memory.available / (1024 * 1024)

    def get_detailed_memory_info(self):
        """Get detailed memory information"""
        memory = psutil.virtual_memory()
        return {
            'total': memory.total / (1024 * 1024),  # MB
            'available': memory.available / (1024 * 1024),  # MB
            'used': memory.used / (1024 * 1024),  # MB
            'percent': memory.percent,
            'free': memory.free / (1024 * 1024)  # MB
        }

    def _clear_file_cache_windows(self):
        """Clear Windows file cache"""
        try:
            result = ctypes.windll.kernel32.SetSystemFileCacheSize(-1, -1, 0)
            if result == 0:
                print("Windows file cache cleared successfully")
                return True
            else:
                print("Failed to clear Windows file cache")
                return False
        except Exception as e:
            print(f"Error clearing Windows file cache: {e}")
            return False

    def _clear_file_cache_linux(self):
        """Clear Linux file cache using multiple methods"""
        methods = [
            (["sudo", "sh", "-c", "echo 3 > /proc/sys/vm/drop_caches"], "sudo echo method"),
            (["sudo", "sysctl", "vm.drop_caches=3"], "sysctl method"),
        ]

        for cmd, method_name in methods:
            try:
                result = subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"Successfully cleared cache using {method_name}")
                    return True
                else:
                    print(f"Failed to clear cache using {method_name}: {result.stderr}")
            except subprocess.TimeoutExpired:
                print(f"Timeout clearing cache using {method_name}")
            except Exception as e:
                print(f"Error clearing cache using {method_name}: {e}")

        print("All Linux cache clearing methods failed. Try: 'sudo sh -c \"echo 3 > /proc/sys/vm/drop_caches\"'")
        return False

    def _clear_process_memory_windows(self):
        """Clear working set of user processes (safely)"""
        cleaned_count = 0
        skipped_system_processes = 0
        failed_count = 0

        # System processes to avoid (case-insensitive)
        system_processes = {
            'system', 'system idle process', 'svchost.exe', 'csrss.exe', 'wininit.exe',
            'winlogon.exe', 'lsass.exe', 'services.exe', 'smss.exe', 'explorer.exe'
        }

        try:
            for process in psutil.process_iter(['pid', 'name']):
                try:
                    process_name = process.info['name']
                    if process_name and process_name.lower() in system_processes:
                        skipped_system_processes += 1
                        continue

                    # Only clean processes that are not system critical
                    handle = ctypes.windll.kernel32.OpenProcess(
                        wintypes.DWORD(0x001F0FFF),  # PROCESS_ALL_ACCESS
                        wintypes.BOOL(False),
                        wintypes.DWORD(process.info['pid'])
                    )

                    if handle:
                        result = ctypes.windll.psapi.EmptyWorkingSet(handle)
                        ctypes.windll.kernel32.CloseHandle(handle)
                        if result == 0:  # Success
                            cleaned_count += 1
                        else:
                            failed_count += 1

                except (psutil.NoSuchProcess, psutil.AccessDenied, OSError) as e:
                    # Skip processes we can't access or that disappear
                    continue
                except Exception as e:
                    print(f"Unexpected error processing {process.info.get('name', 'unknown')}: {e}")
                    continue

            print(f"Cleared memory for {cleaned_count} processes, skipped {skipped_system_processes} system processes")
            if failed_count > 0:
                print(f"Failed to clear memory for {failed_count} processes (access denied or protected)")
            return cleaned_count

        except Exception as e:
            print(f"Error during process memory cleanup: {e}")
            return 0

    def _clear_dlls_windows(self):
        """Clear current process working set"""
        try:
            # This affects the current Python process
            result = ctypes.windll.kernel32.SetProcessWorkingSetSize(-1, -1, -1)
            if result == 0:
                print("Successfully cleared DLL working set")
                return True
            else:
                print("Failed to clear DLL working set")
                return False
        except Exception as e:
            print(f"Error clearing DLL working set: {e}")
            return False

    def _clear_dlls_linux(self):
        """Sync filesystem buffers on Linux"""
        try:
            subprocess.run(["sync"], check=True, capture_output=True, timeout=5)
            print("Successfully synced filesystem buffers")
            return True
        except subprocess.TimeoutExpired:
            print("Timeout syncing filesystem buffers")
            return False
        except Exception as e:
            print(f"Error syncing filesystem buffers: {e}")
            return False

    def clean_ram(self, anything, clean_file_cache, clean_processes, clean_dlls, retry_times, unique_id=None, extra_pnginfo=None):
        """Main RAM cleanup function with improved error handling and safety"""
        if retry_times < 1 or retry_times > 10:
            print(f"Invalid retry_times value: {retry_times}. Using default of 3.")
            retry_times = 3

        try:
            initial_mem = self.get_detailed_memory_info()
            print(f"RAM Cleanup Start - Usage: {initial_mem['percent']:.1f}%, "
                  f"Available: {initial_mem['available']:.1f}MB, "
                  f"Total: {initial_mem['total']:.1f}MB")

            system = platform.system()
            total_cleaned_processes = 0
            operations_completed = []

            for attempt in range(retry_times):
                print(f"\n--- Attempt {attempt + 1}/{retry_times} ---")

                # File cache cleanup
                if clean_file_cache:
                    print("Attempting file cache cleanup...")
                    if system == "Windows":
                        if self._clear_file_cache_windows():
                            operations_completed.append("file_cache")
                    elif system == "Linux":
                        if self._clear_file_cache_linux():
                            operations_completed.append("file_cache")
                    else:
                        print(f"Unsupported platform for file cache cleanup: {system}")

                # Process memory cleanup
                if clean_processes:
                    print("Attempting process memory cleanup...")
                    if system == "Windows":
                        cleaned = self._clear_process_memory_windows()
                        if cleaned > 0:
                            total_cleaned_processes += cleaned
                            operations_completed.append("processes")
                    elif system == "Linux":
                        print("Process memory cleanup not implemented for Linux")
                    else:
                        print(f"Unsupported platform for process cleanup: {system}")

                # DLL/working set cleanup
                if clean_dlls:
                    print("Attempting DLL/working set cleanup...")
                    if system == "Windows":
                        if self._clear_dlls_windows():
                            operations_completed.append("dlls")
                    elif system == "Linux":
                        if self._clear_dlls_linux():
                            operations_completed.append("sync")
                    else:
                        print(f"Unsupported platform for DLL cleanup: {system}")

                # Brief pause between attempts
                if attempt < retry_times - 1:
                    time.sleep(0.5)

                # Progress update
                current_mem = self.get_detailed_memory_info()
                print(f"After attempt {attempt + 1} - Usage: {current_mem['percent']:.1f}%, "
                      f"Available: {current_mem['available']:.1f}MB")

            # Final results
            final_mem = self.get_detailed_memory_info()
            memory_freed = initial_mem['available'] - final_mem['available']

            print(f"\n=== RAM Cleanup Complete ===")
            print(f"Operations completed: {', '.join(operations_completed) if operations_completed else 'None'}")
            print(f"Processes cleaned: {total_cleaned_processes}")
            print(f"Memory freed: {memory_freed:+.1f}MB")
            print(f"Final usage: {final_mem['percent']:.1f}%, Available: {final_mem['available']:.1f}MB")

        except Exception as e:
            print(f"Critical error during RAM cleanup process: {e}")
            import traceback
            traceback.print_exc()

        return (anything,)
    

NODE_NAME = 'RAM Cleanup [RvTools-X]'
NODE_DESC = 'RAM Cleanup'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvSettings_RAMCleanup
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}