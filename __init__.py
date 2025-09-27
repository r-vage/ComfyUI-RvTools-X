# ComfyUI-RvTools-X Extension Loader
#
# Initializes and loads all custom nodes for ComfyUI-RvTools-X, providing NODE_CLASS_MAPPINGS and NODE_DISPLAY_NAME_MAPPINGS for the extension.
#
# Author: r-vage
# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import importlib.util
import os
import __main__
from .core import version, cstr

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# MESSAGE TEMPLATES
cstr.color.add_code("msg", f"{cstr.color.LIGHTGREEN}RvTools-X: {cstr.color.END}")
cstr.color.add_code("warning", f"{cstr.color.LIGHTGREEN}RvTools-X {cstr.color.LIGHTYELLOW}Warning: {cstr.color.END}")
cstr.color.add_code("debug", f"{cstr.color.LIGHTGREEN}RvTools-X {cstr.color.LIGHTBEIGE}Debug: {cstr.color.END}")
cstr.color.add_code("error", f"{cstr.color.RED}RvTools-X {cstr.color.END}Error: {cstr.color.END}")

cstr(f'Version: {version}').msg.print()

def get_ext_dir(subpath=None, mkdir=False):
    dir = os.path.dirname(__file__)
    if subpath is not None:
        dir = os.path.join(dir, subpath)
    dir = os.path.abspath(dir)
    if mkdir and not os.path.exists(dir):
        os.makedirs(dir)
    return dir

py = get_ext_dir("py")
files = os.listdir(py)
for file in files:
    if not file.endswith(".py"):
        continue
    name = os.path.splitext(file)[0]
    imported_module = importlib.import_module(f".py.{name}", __name__)
    try:
        NODE_CLASS_MAPPINGS = {**NODE_CLASS_MAPPINGS, **imported_module.NODE_CLASS_MAPPINGS}
        NODE_DISPLAY_NAME_MAPPINGS = {**NODE_DISPLAY_NAME_MAPPINGS, **imported_module.NODE_DISPLAY_NAME_MAPPINGS}
    except Exception:
        pass

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

WEB_DIRECTORY = "./web"
