# ResumeIQ — Plan

Build 1 scope approved: local paste-and-review app, server-side OpenRouter first, explicit non-AI fallback, PRD, real screenshot, honest log, and documentation. No commit or push before review.

## Architecture

- `server.py`: Python 3.8+ HTTP server; loads environment, serves explicit UI routes, validates input, calls OpenRouter, validates result shape. Binds to 127.0.0.1 only.
- `app/`: plain HTML/CSS/JavaScript. Output uses textContent.
- `docs/`: static Product Page and actual screenshot for GitHub Pages.
- One PDF library (pypdf); standard-library DOCX parsing; no database, login, saved resume history, or Build 1 analytics.
- Default model: `openai/gpt-4o-mini`, overridable with `OPENROUTER_MODEL`. Live availability and quality remain unverified.

## Risk and verification

Main risk: misleading or invented advice. The prompt asks for grounded evidence and forbids invented metrics. Schema checks verify structure and exactly three improvements, not factual correctness.

Completed: five deterministic tests, JavaScript syntax, actual browser non-AI workflow, private-file/invalid-input HTTP checks, mobile width check, screenshot inspection.

Pending: valid key and live AI review; builder demo; reachable PM recruiting student; public Pages deployment. Build 4 track undecided: choose Track A domain evals or Track B user replays using `tests/README.md` later.

## Costs and time

No live inference requests made during implementation. Agent spending, cumulative costs, and builder hours are unknown. No totals or per-run prices inferred. Record actual provider billing after a live run and personal hours on the Product Page.

## Next steps

1. Privately configure `.env`, restart, and review a fictional sample in AI mode.
2. Check grounded strengths, relevant gaps, and three truthful actionable edits.
3. Record actual hours, expenses, personal learning, and feedback only after collecting it.
4. Review changes, then separately authorize commit/push. Publish Pages from `main` → `/docs`.
5. Build 2: test output quality and plan analytics. Never include resume content in analytics.

## Approved upload extension

PDF and .docx upload → `/api/extract` → editable resume text → existing analysis workflow. Files stay in memory. Limits: 5 MB, 20 PDF pages, 20,000 extracted characters. Errors preserve existing text. No OCR or legacy .doc support. Use a virtual environment and `requirements.txt`; see README. Ten tests passed, including PDF/DOCX extraction and upload-to-analysis HTTP checks. Complex document reading order and real-user documents still need manual review.
