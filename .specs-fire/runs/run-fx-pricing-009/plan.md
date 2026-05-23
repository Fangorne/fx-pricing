---
run: run-fx-pricing-009
work_item: github-actions-ci
intent: docker-ci-setup
mode: confirm
generated: "2026-05-23T12:05:00Z"
---

# Plan: GitHub Actions CI (lint + test)

## Files to Create

| File | Purpose |
|------|---------|
| `.github/workflows/ci.yml` | CI workflow — 2 parallel jobs: lint and test |

## Key Config

- Triggers: push and pull_request targeting main
- lint job: ruff check → ruff format --check → mypy app/
- test job: pytest --cov=app --cov-report=xml → upload coverage.xml artifact
- uv setup: astral-sh/setup-uv@v3, cache key on pyproject.toml + uv.lock hash
- uv sync --frozen --extra dev for reproducibility
- working-directory: backend on all steps
- Python 3.12 via actions/setup-python@v5
- Both jobs parallel (no needs: dependency)
