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

### Bundle Entry Skill

- [using-dify-dsl](skills/using-dify-dsl/SKILL.md)  
  Handles intent recognition, permission-boundary judgment, and primary skill routing. If you install this repository as one skill bundle, start here first.

Only the bundle entry skill currently keeps `agents/openai.yaml`. The downstream `dify-dsl-*` skills are still independent skills discovered from their `SKILL.md` files.

### Entry Skills

- [dify-dsl-subagent-review](skills/dify-dsl-subagent-review/SKILL.md)  
  Use when a Dify DSL task needs formal multi-review orchestration, subagent fallback, or conflict merge before a final conclusion.
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

### Subagent Review Overview

- [Dify DSL Subagent Review Overview](docs/dify-dsl-subagent-review-overview.md)  
  A one-page summary of when to use `dify-dsl-subagent-review`, how its four modes work, which roles are involved, and what the current repository coverage looks like.

## How To Use This Repository

If you install the whole repository as one skill bundle, the simplest entry is [using-dify-dsl](skills/using-dify-dsl/SKILL.md). It decides which downstream skill should handle the user request.

### Quick Path

<!-- BEGIN ROUTE_MATRIX -->
| User goal | Recommended entry | Common next step |
| --- | --- | --- |
| Requirements still unclear | `using-dify-dsl` or `dify-dsl-brainstorming` | `dify-dsl-authoring / review / refactor` |
| Create a new DSL | `using-dify-dsl` or `dify-dsl-authoring` | Use `dify-dsl-subagent-review` when complexity or risk is high |
| Review an existing DSL read-only | `using-dify-dsl` or `dify-dsl-review` | Escalate to `dify-dsl-subagent-review` for formal multi-review |
| Modify an existing DSL | `using-dify-dsl` or `dify-dsl-refactor` | Use `dify-dsl-subagent-review` after risky changes |
| Only choose a template | `using-dify-dsl` or `dify-dsl-templates` | Move to `dify-dsl-authoring` if a full draft is needed |
| Only decide whether it is deliverable | `using-dify-dsl` or `dify-dsl-governance` | Use `dify-dsl-subagent-review` first only when the user explicitly wants multi-review or conflict merge |
| Explicitly organize multi-review | `using-dify-dsl` or `dify-dsl-subagent-review` | Pick parallel / serial / single-subagent / no-subagent fallback |
<!-- END ROUTE_MATRIX -->

The main path is:

<!-- BEGIN MAIN_PATH -->
```text
using-dify-dsl
-> brainstorming / authoring / review / refactor / templates / governance / subagent-review
-> use subagent-review or governance again only when needed
```
<!-- END MAIN_PATH -->

If you already know the exact goal, you can still jump directly to an entry skill:

- requirements unclear: start with [dify-dsl-brainstorming](skills/dify-dsl-brainstorming/SKILL.md)
- create a new DSL: start with [dify-dsl-authoring](skills/dify-dsl-authoring/SKILL.md)
- review an existing DSL read-only: start with [dify-dsl-review](skills/dify-dsl-review/SKILL.md)
- modify an existing DSL: start with [dify-dsl-refactor](skills/dify-dsl-refactor/SKILL.md)
- organize multi-review and merge conclusions: start with [dify-dsl-subagent-review](skills/dify-dsl-subagent-review/SKILL.md)
- validate the skills themselves: start with [dify-dsl-forward-testing](skills/dify-dsl-forward-testing/SKILL.md)

## Install For Codex

The recommended setup is to install the whole repository as one bundle instead of symlinking each skill separately into `~/.codex/skills/`.

See [.codex/INSTALL.md](.codex/INSTALL.md) for the manual steps and the migration script.

Current Codex builds may still list multiple downstream `dify-dsl-*` skills in the picker even when installed as a bundle. Treat `using-dify-dsl` as the recommended entry, not as the only visible card.

## Repository Layout

```text
tee/
├── .codex/INSTALL.md
├── .github/workflows/validate.yml
├── docs/
│   ├── dify-dsl-subagent-review-overview.md
│   └── dify-dsl-subagent-review-overview.zh-CN.md
├── scripts/
│   ├── install_codex_bundle.sh
│   ├── quick_validate.py
│   ├── validate_skill_repo.py
│   └── validate_forward_testing.py
├── skills/
│   ├── using-dify-dsl/
│   ├── dify-dsl-subagent-review/
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

- keep the bundle entry skill at `skills/using-dify-dsl/`
- keep domain skills under `skills/dify-dsl-*`
- keep shared DSL fixtures under `tests/fixtures/dsl/`
- if you changed the quick route tables or main path snippets, run `python3 scripts/route_matrix_docs.py --write` to resync generated docs
- when adding or changing a case, try to add:
  - `oracle.json`
  - `replay-output.txt`
  - `expectation_files`
- if a change affects skill coordination, at minimum run:

```bash
python3 scripts/quick_validate.py
python3 scripts/validate_forward_testing.py
```
