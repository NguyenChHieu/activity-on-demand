"""Command line interface for generating Sugar activity bundles."""

from __future__ import annotations

import argparse
import shutil
import sys
from importlib import resources
from pathlib import Path

from .bundler import bundle_activity
from .generator import Generator
from .validator import validate_activity


def _copy_template(template_name: str, destination_root: Path) -> Path:
    template_root = resources.files("activity_on_demand.templates").joinpath(template_name)
    destination = destination_root / template_name
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(template_root, destination)
    return destination


def cmd_init(args: argparse.Namespace) -> int:
    prompt = args.prompt
    if prompt is None and sys.stdin.isatty():
        prompt = input("Describe the Sugar activity (optional): ").strip() or None
    generator = Generator()
    spec, _ = generator.render(prompt, name=args.name)
    destination_root = Path(args.output).resolve()
    destination_root.mkdir(parents=True, exist_ok=True)

    activity_dir = _copy_template("HelloGenerated.activity", destination_root)
    info_path = activity_dir / "activity" / "activity.info"
    main_path = activity_dir / "main.py"

    info_path.write_text(
        info_path.read_text(encoding="utf-8").format(
            name=spec.name,
            bundle_id=spec.bundle_id,
            class_name=spec.class_name,
            version=spec.version,
            command=spec.command,
        ),
        encoding="utf-8",
    )
    main_path.write_text(
        main_path.read_text(encoding="utf-8").format(
            name=spec.name,
            class_name=spec.class_name,
        ),
        encoding="utf-8",
    )

    if spec.directory_name != activity_dir.name:
        renamed = activity_dir.with_name(spec.directory_name)
        if renamed.exists():
            shutil.rmtree(renamed)
        activity_dir.rename(renamed)
        activity_dir = renamed

    print(f"Initialized Sugar activity at {activity_dir}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    errors = validate_activity(args.activity_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Validation passed for {args.activity_dir}")
    return 0


def cmd_bundle(args: argparse.Namespace) -> int:
    source = Path(args.activity_dir).resolve()
    errors = validate_activity(source)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    bundled = bundle_activity(source, args.output)
    print(f"Bundled Sugar activity to {bundled}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate and manage Sugar activity bundles.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Generate a minimal Sugar activity directory.")
    init_parser.add_argument("--name", default="HelloGenerated", help="Activity name to generate.")
    init_parser.add_argument("--output", default=".", help="Directory where the activity should be created.")
    init_parser.add_argument("--prompt", help="Optional prompt describing the activity.")
    init_parser.set_defaults(func=cmd_init)

    validate_parser = subparsers.add_parser("validate", help="Validate a Sugar activity directory.")
    validate_parser.add_argument("activity_dir", help="Path to the .activity directory.")
    validate_parser.set_defaults(func=cmd_validate)

    bundle_parser = subparsers.add_parser("bundle", help="Assemble a validated Sugar activity into an output directory.")
    bundle_parser.add_argument("activity_dir", help="Path to the .activity directory.")
    bundle_parser.add_argument("--output", default="dist", help="Directory where the bundled activity should be copied.")
    bundle_parser.set_defaults(func=cmd_bundle)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
