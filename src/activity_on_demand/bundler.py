"""Bundling helpers for assembling Sugar activity directories."""

from __future__ import annotations

import shutil
from pathlib import Path


def bundle_activity(source_dir: str | Path, output_dir: str | Path) -> Path:
    """Copy a generated activity directory into the requested output directory."""

    source = Path(source_dir)
    destination_root = Path(output_dir)
    destination_root.mkdir(parents=True, exist_ok=True)
    destination = destination_root / source.name

    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)
    return destination
