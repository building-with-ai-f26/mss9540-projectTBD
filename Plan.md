# ResumeIQ — Plan

Build 1 scope approved: local paste-and-review app, server-side OpenRouter first, explicit non-AI fallback, PRD, real screenshot, honest log, and documentation. No commit or push before review.

## Architecture

- `server.py`: Python 3.8+ HTTP server; loads environment, serves explicit UI routes, validates input, calls OpenRouter, validates result shape. Binds to 127.0.0.1 only.
- `app/`: plain HTML/CSS/JavaScript. Output uses textContent.
- `docs/`: static Product Page and actual screenshot for GitHub Pages.
- One PDF library (pypdf); standard-library DOCX parsing; no database, login, saved resume history, or Build 1 analytics.
- Default model: `openai/gpt-4o-mini`, overridable with `OPENROUTER_MODEL`. The builder’s November 12 fictional-example review succeeded, as captured in `docs/assets/ai-review.png`. Systematic model quality remains unverified.

## Risk and verification

Main risk: misleading or invented advice. The prompt asks for grounded evidence and forbids invented metrics. Schema checks verify structure and exactly three improvements, not factual correctness.

Completed: ten deterministic tests and JavaScript syntax checks rerun November 12. Earlier browser checks covered the non-AI workflow, private-file/invalid-input HTTP routes, and mobile width. The builder supplied a screenshot of a successful live AI review on November 12; the Product Page now includes that actual output alongside the earlier non-AI screenshot.

Pending: systematic model quality checks; outside target-user review; public Pages deployment verification. Build 4 track undecided: choose Track A domain evals or Track B user replays using `tests/README.md` later.

## Costs and time

Coding-agent subscription: approximately $20/month (builder estimate), shared with other uses; ResumeIQ’s portion has not been measured. OpenRouter: $5 in prepaid credits purchased (builder-reported). Estimated runtime API cost: $0.0003–$0.0007 per short fictional-example GPT-4o mini review, excluding credit-purchase fees. This is an estimate; actual API usage charges and cumulative project costs have not been reported. Builder time: approximately 3 hours (previously reported estimate). Pricing and billing links are in the Product Page build log.

## Next steps

1. Review the captured successful AI output; add experience or metrics only when supported by actual evidence.
2. Check grounded strengths, relevant gaps, and three truthful actionable edits.
3. Record actual API usage charges and any revised hours or expenses when available; collect outside feedback before claiming user outcomes.
4. Review changes, then separately authorize commit/push. Publish Pages from `main` → `/docs`.
5. Build 2: test output quality and plan analytics. Never include resume content in analytics.

## Approved upload extension

PDF and .docx upload → `/api/extract` → editable resume text → existing analysis workflow. Files stay in memory. Limits: 5 MB, 20 PDF pages, 20,000 extracted characters. Errors preserve existing text. No OCR or legacy .doc support. Use a virtual environment and `requirements.txt`; see README. Ten tests passed, including PDF/DOCX extraction and upload-to-analysis HTTP checks. Complex document reading order and real-user documents still need manual review.
