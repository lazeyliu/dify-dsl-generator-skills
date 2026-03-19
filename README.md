# tee

[简体中文](README.zh-CN.md)

`tee` is a skill repository for working with `Dify DSL`.

It is not an application repository and it is not just a template collection. It provides a structured set of skills, references, fixtures, and validation scripts for AI agents that need to design, generate, review, refactor, and validate `Dify Workflow`, `Chatflow`, and `RAG Pipeline` DSL.

## What This Project Is

This project treats `Dify DSL` as an orchestration system that needs to be designed, generated, reviewed, repaired, refactored, and validated.

Its core value comes from three things:

- splitting DSL capabilities into focused, composable skills instead of one large prompt
- separating node knowledge, templates, review rules, and governance rules into reusable foundations
- turning “the agent seems capable” into something testable with fixtures, cases, replays, reports, and diffs

## What Problems It Solves

The hard part of working with Dify DSL is usually not “writing YAML.” The real problems are:

- unclear mode selection across `workflow`, `advanced-chat`, and `rag_pipeline`
- fragile node fields, selectors, edges, and container closure
- mixing templates, node knowledge, review rules, and delivery judgment in the same context
- conclusions without evidence, replay coverage, or regression checks

This repository exists to solve those problems.

## Supported Scope

The current skill set covers:

- `kind: app` + `app.mode: workflow`
- `kind: app` + `app.mode: advanced-chat`
- `kind: rag_pipeline`

## Skill Set

### Entry Skills

- [dify-dsl-brainstorming](skills/dify-dsl-brainstorming/SKILL.md)  
  Use when requirements are still unclear and unknowns need to be resolved before moving forward.
- [dify-dsl-authoring](skills/dify-dsl-authoring/SKILL.md)  
  Use to generate a DSL draft from clear requirements.
- [dify-dsl-review](skills/dify-dsl-review/SKILL.md)  
  Use for read-only review, risk grading, import judgment, and release conclusions.
- [dify-dsl-refactor](skills/dify-dsl-refactor/SKILL.md)  
  Use for minimal fixes, optimization, and structural refactoring.

### Foundation Skills

- [dify-dsl-foundations](skills/dify-dsl-foundations/SKILL.md)  
  Mode selection, routing, field conventions, output contracts, and validation contracts.
- [dify-dsl-nodes](skills/dify-dsl-nodes/SKILL.md)  
  Node knowledge, node combinations, container rules, and selector rules.
- [dify-dsl-templates](skills/dify-dsl-templates/SKILL.md)  
  Template library, skeletons, validation status, and variants.
- [dify-dsl-quality](skills/dify-dsl-quality/SKILL.md)  
  Review, repair, optimization, and reviewer role split.
- [dify-dsl-governance](skills/dify-dsl-governance/SKILL.md)  
  Release judgment, change impact, coverage, observability, and capability contracts.

### Validation Skill

- [dify-dsl-forward-testing](skills/dify-dsl-forward-testing/SKILL.md)  
  Use real fixtures, real prompts, replay outputs, and reports to validate that the skill system actually works.

## How To Use This Repository

Pick the entry skill based on the goal:

- requirements unclear: start with [dify-dsl-brainstorming](skills/dify-dsl-brainstorming/SKILL.md)
- create a new DSL: start with [dify-dsl-authoring](skills/dify-dsl-authoring/SKILL.md)
- review an existing DSL read-only: start with [dify-dsl-review](skills/dify-dsl-review/SKILL.md)
- modify an existing DSL: start with [dify-dsl-refactor](skills/dify-dsl-refactor/SKILL.md)
- validate the skills themselves: start with [dify-dsl-forward-testing](skills/dify-dsl-forward-testing/SKILL.md)

## Repository Layout

```text
tee/
├── .github/workflows/validate.yml
├── scripts/
│   ├── quick_validate.py
│   ├── validate_skill_repo.py
│   └── validate_forward_testing.py
├── skills/
│   ├── dify-dsl-brainstorming/
│   ├── dify-dsl-authoring/
│   ├── dify-dsl-review/
│   ├── dify-dsl-refactor/
│   ├── dify-dsl-foundations/
│   ├── dify-dsl-nodes/
│   ├── dify-dsl-templates/
│   ├── dify-dsl-quality/
│   ├── dify-dsl-governance/
│   └── dify-dsl-forward-testing/
├── tests/
│   └── fixtures/dsl/
└── .forward-testing/
```

## Shared Resources

Shared DSL fixtures live in `tests/fixtures/dsl/`.

Forward-testing outputs are written to `.forward-testing/`:

- `last-good.json`
- `latest-report.json`
- `latest-diff.json`

## Common Commands

Validate repository structure:

```bash
python3 scripts/quick_validate.py
```

Run forward testing:

```bash
python3 scripts/validate_forward_testing.py
```

Promote the current result to the stable baseline:

```bash
python3 scripts/validate_forward_testing.py --promote-current
```

If you want to run lower-level validation scripts directly:

```bash
python3 skills/dify-dsl-foundations/scripts/fast_test_dsl.py <sample.yml>
python3 skills/dify-dsl-foundations/scripts/fast_test_suite.py <sample.yml|directory> [...]
python3 skills/dify-dsl-forward-testing/scripts/run_validation_suite.py [--json-out <report.json>]
python3 skills/dify-dsl-forward-testing/scripts/compare_validation_reports.py <old.json> <new.json> [--json-out <diff.json>]
```

## Automation

The GitHub Actions workflow is in [validate.yml](.github/workflows/validate.yml).

It runs two jobs:

- `structure`  
  runs `python3 scripts/quick_validate.py`
- `forward-testing`  
  runs `python3 scripts/validate_forward_testing.py`

The `forward-testing` job uploads `.forward-testing/latest-report.json` as an artifact.

## Maintenance Notes

- keep new skills under `skills/dify-dsl-*`
- keep shared DSL fixtures under `tests/fixtures/dsl/`
- when adding or changing a case, try to add:
  - `oracle.json`
  - `replay-output.txt`
  - `expectation_files`
- if a change affects skill coordination, at minimum run:

```bash
python3 scripts/quick_validate.py
python3 scripts/validate_forward_testing.py
```
