### Project Idea: Sugar Activity on Demand

Generate Sugar learning activities automatically from natural language prompts using AI-oriented scaffolding.

## Package layout

The project now exposes a Python package under `src/activity_on_demand/` with these core modules:

- `cli.py` — command parsing, prompt capture, and command dispatch.
- `generator.py` — placeholder orchestration for future LLM/spec generation.
- `validator.py` — validation of required Sugar activity files.
- `bundler.py` — assembly of generated activity bundles.
- `templates/` — starter files for `HelloGenerated.activity`.

## Commands

Run the package directly:

```bash
python -m activity_on_demand init --output build
python -m activity_on_demand validate build/HelloGenerated.activity
python -m activity_on_demand bundle build/HelloGenerated.activity --output dist
```

Or use the installed console script:

```bash
activity-on-demand init
```

## Generated Sugar layout

The generated activity follows Sugar conventions:

```text
<Name>.activity/
  activity/activity.info
  main.py
  icons/
  assets/
```
