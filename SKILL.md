---
name: openclaw_reference
description: Reference OpenClaw source documentation for product usage, deployment, configuration, CLI commands, channels, gateway behavior, tools, and troubleshooting. Use when users ask how OpenClaw works, how to configure or operate it, where a feature is documented, or to verify behavior from docs before answering.
---

# OpenClaw Reference

Use this skill to answer OpenClaw questions from local source docs in `openclaw_docs/`, not memory.

## Files

- `./openclaw_docs/`: markdown source docs
- `./docs.json`: optional metadata/navigation mapping
- `./references/routing-cheatsheet.md`: intent-to-path quick router for broad questions
- `./references/query-examples.md`: ready-to-use search query patterns by user intent

## Workflow

1. Identify intent and route to likely subdirectories first.
   - If intent is broad or mixed, read `references/routing-cheatsheet.md` first.
   - If wording is clear but query terms are weak, read `references/query-examples.md`.
2. Search with fast text search (`rg`) under `openclaw_docs/`; avoid broad full-tree reads.
3. Read full content of the top 1-3 most relevant files before answering.
4. Synthesize a direct answer and include exact file paths used.
5. If docs are ambiguous or missing, say so explicitly and state what was searched.

## Routing Hints

- Getting started/install/platform setup: `start/`, `install/`, `platforms/`
- Runtime model and behavior: `concepts/`, `gateway/`, `tools/`
- CLI commands: `cli/`
- Integrations/providers: `providers/`, `channels/`, `plugins/`, `nodes/`
- Failures and debugging: `help/`, `diagnostics/`, `gateway/troubleshooting.md`, `channels/troubleshooting.md`
- Security topics: `security/`, `tools/exec-approvals.md`, `gateway/security/`
- Experimental or planning material: `experiments/` (only use when user asks for proposals/plans)

## Search and Read Strategy

- Start with targeted queries, then widen only if needed.
- Prefer searching filenames first, then file content.
- Exclude merged or generated outputs when present.
- For very large files, jump to relevant sections first, then expand for surrounding context.
- Do not rely on a single snippet when explaining behavior, constraints, or defaults.

## Answer Quality Bar

- Ground each key claim in files actually read.
- Include paths in the response so users can verify quickly.
- Separate documented behavior from inference.
- Do not invent flags, defaults, commands, or config keys not found in docs.
