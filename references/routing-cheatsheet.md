# OpenClaw Routing Cheatsheet

Use this file when the user question is broad and you need a fast first route before full-text search.

## User Intent -> First Paths

- Install, upgrade, uninstall, migration:
  - `openclaw_docs/install/`
  - `openclaw_docs/start/`
  - `openclaw_docs/platforms/`
- Product architecture, runtime behavior, model/session concepts:
  - `openclaw_docs/concepts/`
  - `openclaw_docs/gateway/`
- CLI command usage:
  - `openclaw_docs/cli/`
- Tool behavior and permissions:
  - `openclaw_docs/tools/`
  - `openclaw_docs/gateway/sandboxing.md`
  - `openclaw_docs/gateway/sandbox-vs-tool-policy-vs-elevated.md`
- Channel integrations (Telegram, Slack, Discord, etc.):
  - `openclaw_docs/channels/`
- Model providers and API backends:
  - `openclaw_docs/providers/`
- Nodes/plugins and extensions:
  - `openclaw_docs/nodes/`
  - `openclaw_docs/plugins/`
- Troubleshooting and diagnostics:
  - `openclaw_docs/help/`
  - `openclaw_docs/diagnostics/`
  - `openclaw_docs/gateway/troubleshooting.md`
  - `openclaw_docs/channels/troubleshooting.md`
- Security, threat model, auth hardening:
  - `openclaw_docs/security/`
  - `openclaw_docs/gateway/security/`
  - `openclaw_docs/gateway/authentication.md`
  - `openclaw_docs/gateway/trusted-proxy-auth.md`
- Experimental design/proposals:
  - `openclaw_docs/experiments/`

## Query Patterns

Run filename-first discovery when possible:

```bash
rg --files openclaw_docs | rg 'install|gateway|telegram|approvals|security'
```

Then run content search in narrowed paths:

```bash
rg -n "heartbeat|auth|permission|model failover" openclaw_docs/gateway openclaw_docs/concepts
```

## Guardrails

- Prefer stable docs over experiments unless the user asks for plans/proposals.
- Read the full relevant file before answering behavior/defaults.
- If no direct documentation is found, say that explicitly and list searched paths.
