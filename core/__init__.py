# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

from .keys import *
from .common import *

__all__ = ["keys", "common", "__version__", "version"]

# Determine package version from pyproject.toml when possible so the version
# follows packaging metadata and does not need manual edits.
from pathlib import Path


def _read_pyproject_version() -> str:
	p = Path(__file__).resolve()
	for parent in p.parents:
		candidate = parent / "pyproject.toml"
		if not candidate.exists():
			continue
		txt = candidate.read_text(encoding="utf-8")
		try:
			import tomllib as _toml  # Python 3.11+

			data = _toml.loads(txt)
		except Exception:
			try:
				import toml as _toml  # type: ignore

				data = _toml.loads(txt)
			except Exception:
				data = None

		if isinstance(data, dict):
			project = data.get("project")
			if isinstance(project, dict) and "version" in project:
				v = project.get("version")
				if isinstance(v, str):
					return v
			tool = data.get("tool")
			if isinstance(tool, dict):
				poetry = tool.get("poetry")
				if isinstance(poetry, dict) and "version" in poetry:
					v = poetry.get("version")
					if isinstance(v, str):
						return v

		# Fallback regex
		import re

		m = re.search(r"\bversion\s*=\s*['\"]([^'\"]+)['\"]", txt)
		if m:
			return m.group(1)

	# Final fallback
	# Historically the project used version "2.5.0"; use it as a safer
	# fallback when pyproject.toml can't be parsed.
	return "2.5.0"


__version__ = _read_pyproject_version()
version = __version__
