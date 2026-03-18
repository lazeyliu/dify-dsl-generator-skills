# dify-dsl-generator

[English](./README.md) | [简体中文](./README.zh-CN.md)

A general-purpose Codex skill for generating, reviewing, analyzing, optimizing, and repairing Dify DSLs, including:

- `kind: app` with `workflow`
- `kind: app` with `advanced-chat`
- `kind: rag_pipeline`

The goal of this skill is not just to produce a YAML file, but to treat a Dify DSL as a system that can be reviewed, tuned, validated, and governed.

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

In a Codex environment that supports skills, invoke it explicitly like this:

```text
Use $dify-dsl-generator to review this Dify DSL and provide structured recommendations.
```

Typical uses include:

- reviewing an existing DSL without modifying files
- brainstorming how to improve the current DSL
- listing nodes, edges, impact areas, and risks before making changes
- producing a review report, release-gate result, and tuning suggestions after changes

## Review and Governance Characteristics

This skill emphasizes:

- human-readable conclusions first, structured detail second
- graded findings using `blocking / high-risk / medium-risk / optimization`
- multi-agent independent review, with asynchronous parallel and synchronous serial modes
- conflict arbitration instead of simply concatenating multiple review results
- governance items such as change impact, coverage matrix, minimal sufficiency, escalation gates, issue taxonomy, and release gates

## Default Conventions

- Default strategy tier: `strict`
- Coverage pass threshold: applicable path coverage `>= 95%`, and the main path, fallback path, and external-exception path must not be missing
- Default user-facing output: `Markdown`
- Default machine-facing output for API or DSL flow consumption: `JSON`
- Optional output forms: `plain text`, `HTML`

## Directory Structure

```text
dify-dsl-generator/
├── SKILL.md
├── README.md
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
  The main file Codex uses to trigger and execute the skill.
- `agents/openai.yaml`
  UI and invocation metadata.
- `references/`
  On-demand reference material, review rules, templates, and governance guidance.
- `README.md`
  Human-facing documentation for GitHub readers and maintainers.

## Maintenance Notes

- When adding or refining review rules, prefer putting details into `references/` instead of growing `SKILL.md`.
- When changing review formats or governance rules, keep `report-template.md`, `review-checklist.md`, and `subagent-review.md` in sync.
- When introducing new defaults, update both `SKILL.md` and the related reference files.

## License

This repository does not yet include a `LICENSE` file.  
If you plan to publish it on GitHub, add an explicit license before release.
