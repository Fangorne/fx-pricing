# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Status

This is a **greenfield project** — no application code exists yet. The repository has the FIRE (Fast Intent-Run Engineering) AI-native development workflow installed.

## Development Workflow: FIRE

All development follows the FIRE methodology. Use these slash commands:

```
/specsmd-fire            # Main entry point — routes automatically based on project state
/specsmd-fire-planner    # Planning only (capture intent, decompose into work items)
/specsmd-fire-builder    # Execution only (run work items, generate walkthroughs)
```

**Flow:** Intent → Work Item → Run, with adaptive checkpoints (0–2):

| Mode | Checkpoints | When |
|------|-------------|------|
| Autopilot | 0 | Low complexity — bug fixes, minor changes |
| Confirm | 1 | Medium complexity — standard features |
| Validate | 2 | High complexity — security, payments, architecture |

## FIRE Artifacts (created on first `/specsmd-fire` run)

```
.specs-fire/
├── state.yaml                     # Central source of truth for all FIRE state
├── standards/                     # constitution.md, tech-stack.md, coding-standards.md, etc.
├── intents/{intent-id}/
│   ├── brief.md
│   └── work-items/{work-item-id}.md
└── runs/{run-id}/
    ├── run.md, plan.md, walkthrough.md, test-report.md, review-report.md
```

`constitution.md` is always loaded from root and cannot be overridden. Other standards can be overridden per module in a monorepo by placing a `.specs-fire/standards/` folder inside the module.

## Key Conventions

- Run IDs: `run-{worktree}-{NNN}` (e.g., `run-fx-pricing-001`)
- Intent and work-item IDs: kebab-case
- `state.yaml` is the authoritative record of all intents, work items, and runs — read it before assuming project state
