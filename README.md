# dify-dsl-generator

[English](./README.md) | [简体中文](./README.zh-CN.md)

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
└── references/
    ├── common-dsl.md
    ├── graded-review-model.md
    ├── report-template.md
    ├── review-checklist.md
    ├── subagent-review.md
    ├── evaluation-gates.md
    ├── coverage-matrix.md
    ├── observability-contract.md
    ├── capability-contracts.md
    └── ...
```

## Directory Notes

- `SKILL.md`
  The portable core workflow and operating instructions.
- `agents/openai.yaml`
  Adapter metadata for OpenAI / Codex, used for platform-specific display and invocation.
- `references/`
  On-demand reference material, review rules, templates, and governance guidance.
- `README.md`
  Human-facing English documentation for GitHub readers and maintainers.
- `README.zh-CN.md`
  Human-facing Simplified Chinese documentation for GitHub readers and maintainers.
- `LICENSE`
  The repository license file.

## Maintenance Notes

- When adding or refining review rules, prefer putting details into `references/` instead of growing `SKILL.md`.
- When changing review formats or governance rules, keep `report-template.md`, `review-checklist.md`, and `subagent-review.md` in sync.
- When introducing new defaults, update both `SKILL.md` and the related reference files.
- When adding support for another agent platform, prefer adding a separate adapter file under `agents/` instead of changing the portable core.

## License

This repository is licensed under the [MIT License](./LICENSE).
