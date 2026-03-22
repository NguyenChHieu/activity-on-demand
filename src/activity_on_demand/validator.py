"""Validation utilities for generated Sugar activity bundles."""

from __future__ import annotations

from pathlib import Path

REQUIRED_PATHS = (
    "activity/activity.info",
    "main.py",
    "icons",
    "assets",
)


def validate_activity(activity_dir: str | Path) -> list[str]:
    """Return a list of validation errors for a Sugar activity directory."""

    root = Path(activity_dir)
    errors: list[str] = []

    if not root.exists():
        return [f"Activity directory does not exist: {root}"]

    if root.suffix != ".activity":
        errors.append("Activity directory should end with '.activity'.")

    for relative_path in REQUIRED_PATHS:
        path = root / relative_path
        if path.suffix or relative_path.endswith(".py") or relative_path.endswith(".info"):
            if not path.is_file():
                errors.append(f"Missing required file: {relative_path}")
        elif not path.is_dir():
            errors.append(f"Missing required directory: {relative_path}")

    info_path = root / "activity" / "activity.info"
    if info_path.is_file():
        content = info_path.read_text(encoding="utf-8")
        for key in ("name =", "bundle_id =", "exec =", "activity_version ="):
            if key not in content:
                errors.append(f"activity.info is missing required field: {key[:-2]}")

    return errors
