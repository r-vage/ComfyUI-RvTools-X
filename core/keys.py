# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from enum import Enum
from typing import Iterable

__all__ = ["TEXTS", "CATEGORY", "KEYS", "category_display"]


class TEXTS(Enum):
    CUSTOM_NODE_NAME = "RvTools-X"
    LOGGER_PREFIX = "RvTools-X"
    CONCAT = "concatenated"
    INACTIVE_MSG = "inactive"
    INVALID_METADATA_MSG = "Invalid metadata raw"
    FILE_NOT_FOUND = "File not found!"


class CATEGORY(Enum):
    MAIN = "🫦 RvTools-X"
    CHECKPOINT = "/ Loader"
    CONVERSION = "/ Conversion"
    FOLDER = "/ Folder"
    IMAGE = "/ Image"
    PASSER = "/ Passer"
    PIPE = "/ Pipe"
    PRIMITIVE = "/ Primitives"
    SETTINGS = "/ Settings"
    SWITCHES = "/ Switches"
    MULTISWITCHES = "/ Multi-Switches"
    TEXT = "/ Text"
    VIDEO = "/ Video"


def category_display(cat: "CATEGORY") -> str:
    # Return a cleaned, human-friendly string for a CATEGORY value.
    #
    # This strips any leading slashes and surrounding whitespace so it can be
    # shown in UIs without duplicated separators.
    # type: ignore[name-defined]
    return cat.value.lstrip("/ ").strip()


# remember, all keys should be in lowercase!
class KEYS(Enum):
    LIST = "list_string"
    PREFIX = "prefix"


# Sanity check: ensure KEYS values are lowercase to match downstream usage.
def _assert_keys_lowercase(items: Iterable[KEYS]) -> None:
    for k in items:
        if k.value != k.value.lower():
            raise AssertionError(f"KEYS value must be lowercase: {k!r}")


_assert_keys_lowercase(KEYS)
