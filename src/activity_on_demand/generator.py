"""Generation orchestration helpers for Sugar activities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ActivitySpec:
    """Minimal specification for a generated Sugar activity."""

    name: str
    bundle_id: str
    class_name: str
    version: str = "1"
    command: str = "sugar-activity3 main.py"

    @property
    def directory_name(self) -> str:
        return f"{self.name}.activity"


class Generator:
    """Placeholder orchestration layer for future LLM-backed generation."""

    def create_spec(self, prompt: str | None = None, *, name: str = "HelloGenerated") -> ActivitySpec:
        cleaned = "".join(ch for ch in name if ch.isalnum() or ch in {" ", "_", "-"}).strip()
        if any(sep in cleaned for sep in (" ", "_", "-")):
            normalized = "".join(part[:1].upper() + part[1:] for part in cleaned.replace("-", " ").replace("_", " ").split())
        else:
            normalized = "".join(ch for ch in cleaned if ch.isalnum())
        normalized = normalized or "HelloGenerated"
        bundle_id = f"org.sugarlabs.{normalized.lower()}"
        return ActivitySpec(
            name=normalized,
            bundle_id=bundle_id,
            class_name=f"{normalized}Activity",
        )

    def render(self, prompt: str | None = None, *, name: str = "HelloGenerated") -> tuple[ActivitySpec, Path]:
        spec = self.create_spec(prompt, name=name)
        return spec, Path(spec.directory_name)
