# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import os
import logging

# Configuration for RvTools-X logger. Allow env override RVTOOLSX_LOGLEVEL
CONFIG = {
    "loglevel": int(os.environ.get("RVTOOLSX_LOGLEVEL", logging.INFO)),
    "indent": int(os.environ.get("RVTOOLSX_INDENT", 2)),
}
