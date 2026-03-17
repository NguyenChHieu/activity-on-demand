### Project Idea: Sugar Activity on Demand

Goal:
Generate Sugar learning activities automatically from natural language prompts using AI.

Example:

```
Prompt:
"Create a multiplication quiz for grade 3 students"
```

System generates:

```
MultiplicationQuiz.activity/
  activity.info
  main.py
  assets/
```

The generated activity can then be installed and launched in Sugar.

---

# Proposed System Architecture

```
User prompt
   ↓
LLM generation
   ↓
Activity specification (JSON)
   ↓
Template engine
   ↓
Activity code generation
   ↓
Validation
   ↓
Activity bundle
   ↓
Launch inside Sugar
```

---

# Core Components of the System

### Prompt interface

CLI or web UI for generating activities.

### LLM generator

Large language model generates activity code or specifications.

### Template engine

Converts generated specification into valid Sugar activity structure.

### Validation layer

Checks:

* required files
* dependencies
* execution entry point

### Activity bundler

Packages activity into `.activity` directory.

### Runner

Installs and launches the generated activity.

---
