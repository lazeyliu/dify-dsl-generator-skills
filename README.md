# dify-dsl-generator

[English](README.md) | [简体中文](README.zh-CN.md)

A general-purpose agent skill for generating, reviewing, analyzing, optimizing, and repairing Dify DSLs, including:

- `kind: app` with `workflow`
- `kind: app` with `advanced-chat`
- `kind: rag_pipeline`

The goal of this skill is not just to produce a YAML file, but to treat a Dify DSL as a system that can be reviewed, tuned, validated, and governed.

Its core workflow is platform-neutral:

- `SKILL.md` and `references/` are the portable core
- `agents/openai.yaml` is the current adapter metadata for OpenAI / Codex
- other agent systems can still reuse the core workflow even if they ignore this adapter file

## Use Cases

This skill is intended for tasks such as:

- creating a new Dify DSL from scratch
- modifying an existing DSL
- reviewing a DSL in read-only mode without changing files
- brainstorming and analyzing the current DSL before making changes
- producing structured review reports, release gates, and tuning suggestions

## Core Capabilities

- DSL generation: choose mode, choose template, fill required fields, selectors, and failure paths
- DSL repair: fix structural issues, compatibility issues, and graph closure problems
- DSL review: syntax checks, model/entity checks, independent review, and graded review
- DSL analysis: read-only analysis of the current DSL with risks, findings, and optimization suggestions
- DSL optimization: improve accuracy, stability, observability, and orchestration flexibility
- DSL governance: support change-impact review, coverage matrix, release gates, observability contracts, and capability contracts

## Invocation

In a Codex or compatible agent environment that supports explicit skill-style invocation, use:

```text
Use $dify-dsl-generator to review this Dify DSL and provide structured recommendations.
```

Typical uses include:

- reviewing an existing DSL without modifying files
- brainstorming how to improve the current DSL
- listing nodes, edges, impact areas, and risks before making changes
- producing a review report, release-gate result, and tuning suggestions after changes

If another agent platform does not support the same invocation or metadata model, the recommended fallback is:

- load `SKILL.md`
- start from `references/index.md`
- start from `references/foundations/task-routing.md`
- load only the needed files from `references/`
- execute the workflow in read-only review, modification, or analysis mode as appropriate

## Review and Governance Characteristics

This skill emphasizes:

- human-readable conclusions first, structured detail second
- graded findings using `blocking / high-risk / medium-risk / optimization`
- multi-agent independent review, with asynchronous parallel and synchronous serial modes
- conflict arbitration instead of simply concatenating multiple review results
- governance items such as change impact, coverage matrix, minimal sufficiency, escalation gates, issue taxonomy, and release gates

## Platform Compatibility

This repository is designed to be reusable across agent ecosystems.

- OpenAI / Codex:
  Uses `agents/openai.yaml` as the current adapter metadata.
- Claude / Qwen / other agents:
  Can reuse `SKILL.md` and `references/` as the portable core.
- If subagents are not available:
  Degrade to sequential review or self-review instead of assuming multi-agent review is always possible.
- If platform-specific metadata is needed:
  Add a separate adapter file instead of modifying the portable core.

In other words:

- the skill definition lives in `SKILL.md`
- the operational detail lives in `references/`
- adapter metadata lives under `agents/`

The current repository ships an OpenAI / Codex adapter, but the skill itself is not limited to OpenAI / Codex.

## Default Conventions

- Default strategy tier: `strict`
- Coverage pass threshold: applicable path coverage `>= 95%`, and the main path, fallback path, and external-exception path must not be missing
- Default user-facing output: `plain text`
- Default machine-facing output for API or DSL flow consumption: `JSON`
- Optional output forms: `Markdown`, `HTML`

## Directory Structure

```text
dify-dsl-generator/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── LICENSE
├── .gitignore
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── fast_test_dsl.py
│   ├── fast_test_suite.py
│   ├── check_forward_test_cases.py
│   ├── init_forward_test_case.py
│   ├── quick_validate.py
│   └── validate_skill_repo.py
├── tests/
│   ├── cases/
│   ├── prompts/
│   ├── fixtures/
│   │   └── dsl/
│   ├── expectations/
│   └── harness/
│       └── assert_output.py
└── references/
    ├── index.md
    ├── foundations/
    │   ├── index.md
    │   ├── common-dsl.md
    │   ├── task-routing.md
    │   └── validation-contract.md
    ├── nodes/
    │   ├── index.md
    │   ├── node-llm.md
    │   └── ...
    ├── templates/
    │   ├── index.md
    │   ├── template-validation-status.md
    │   └── ...
    ├── quality/
    │   ├── index.md
    │   ├── review-checklist.md
    │   ├── report-template.md
    │   ├── subagent-review.md
    │   └── ...
    └── governance/
        ├── index.md
        ├── evaluation-gates.md
        ├── coverage-matrix.md
        └── ...
```

## Directory Notes

- `SKILL.md`
  The portable core workflow and operating instructions.
- `agents/openai.yaml`
  Adapter metadata for OpenAI / Codex, used for platform-specific display and invocation.
- `references/`
  On-demand reference material, split by theme to keep routing shallow and loading cost low. The canonical top-level entry is `references/index.md`.
- `references/foundations/`
  Entry documents, routing rules, contracts, selectors, shared field references, and the canonical foundation entry page at `references/foundations/index.md`.
- `references/nodes/`
  Per-node documentation and the canonical node entry page at `references/nodes/index.md`.
- `references/templates/`
  Template catalogs, variants, validated skeletons, and the canonical template entry page at `references/templates/index.md`.
- `references/quality/`
  Review, repair, optimization, and the canonical quality entry page at `references/quality/index.md`.
- `references/governance/`
  Release gates, coverage, contracts, observability, and the canonical governance entry page at `references/governance/index.md`.
- `scripts/validate_skill_repo.py`
  Local structural validator for frontmatter, adapter metadata, and markdown link integrity.
- `scripts/quick_validate.py`
  Compatibility wrapper aligned with the standard skill-maintenance validation entrypoint.
- `scripts/fast_test_dsl.py`
  Read-only fast-test helper for profiling a real Dify DSL sample against the repo's routing structure.
- `scripts/fast_test_suite.py`
  Aggregate fast-test coverage across one or more real DSL samples and report which entry routes are still missing.
- `scripts/check_forward_test_cases.py`
  Validate repo-local forward-test cases and aggregate their expected route coverage.
- `scripts/init_forward_test_case.py`
  Initialize a reusable forward-test case directory with `prompt.txt` and `oracle.json`.
- `tests/cases/`
  Reusable forward-test case directories composed from prompts, fixtures, and oracle metadata.
- `tests/prompts/`
  Minimal prompt corpus for explicit skill requests, multiturn follow-up, downgrade pressure, and template-route cases.
- `tests/fixtures/dsl/`
  Local YAML fixtures for workflow, advanced-chat, rag pipeline, and broken-structure smoke tests.
- `tests/expectations/`
  Lightweight expectation files for output order, downgrade language, and final conclusion mapping.
- `tests/harness/assert_output.py`
  Generic text assertion helper for contains/order checks against captured outputs.
- `README.md`
  Human-facing English documentation for GitHub readers and maintainers.
- `README.zh-CN.md`
  Human-facing Simplified Chinese documentation for GitHub readers and maintainers.
- `LICENSE`
  The repository license file.

## Maintenance Notes

- When adding or refining review rules, prefer putting details into `references/` instead of growing `SKILL.md`.
- When changing review formats or governance rules, keep `references/quality/report-template.md`, `references/quality/review-checklist.md`, and `references/quality/subagent-review.md` in sync.
- When introducing new defaults, update both `SKILL.md` and the related reference files.
- After moving files or editing cross-links, run `python3 scripts/quick_validate.py` or `python3 scripts/validate_skill_repo.py`.
- For a realistic artifact smoke test, run `python3 scripts/fast_test_dsl.py <path/to/sample.yml>`.
- For route-coverage aggregation across multiple samples, run `python3 scripts/fast_test_suite.py <sample.yml|directory> [...]`.
- To scaffold a reusable forward-test case, run `python3 scripts/init_forward_test_case.py <case-dir> --target <sample.yml>`.
- To validate repo-local forward-test cases and aggregate expected route coverage, run `python3 scripts/check_forward_test_cases.py`.
- To validate a captured output against a lightweight expectation, run `python3 tests/harness/assert_output.py <expectation.json> <output.txt>`.
- When adding support for another agent platform, prefer adding a separate adapter file under `agents/` instead of changing the portable core.

## License

This repository is licensed under the [MIT License](LICENSE).
