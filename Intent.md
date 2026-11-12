# ResumeIQ — Build 1 Intent

Due November 9, 2026 at noon, New York time. Required PRD and log: [Product Page](docs/index.html).

Primary user: an NYU Stern MBA student recruiting for product management. Planned outreach is a classmate through the builder’s school network. No participant or feedback is confirmed.

Before: manually compare resume and posting and guess what to emphasize. This is a product hypothesis, not validated research.

After: upload a PDF/.docx resume or paste text, paste a job description, review strengths and missing evidence, then make three truthful edits.

One core workflow: resume + specific job description → analysis → three improvements.

Build 1 non-goals:

1. Job-title-only analysis (possible later feature).
2. Resume formatting, template design, and exports.
3. Job searching, application submission, and ATS integrations.

Prototype: `.venv/bin/python server.py` → `http://127.0.0.1:8000`. Screenshots: `docs/assets/prototype.png` (non-AI interface) and `docs/assets/ai-review.png` (successful live AI review, November 12).

Verified: non-AI workflow with fictional inputs, three suggestions, mobile width, validation/private-file routes, and ten deterministic tests (rerun November 12). The builder successfully generated a live OpenRouter review of the fictional example using openai/gpt-4o-mini and supplied the November 12 screenshot. This confirms a working connection; systematic model quality and target-user usefulness remain unverified. Keyword comparison cannot assess qualifications or quality. No user outcomes are claimed.

Scope update approved by builder: PDF and Word .docx uploads now extract text locally into the editable resume field. Scanned PDFs and legacy .doc files remain unsupported. Ten automated tests pass, including extraction and HTTP upload-to-review checks with generated fictional documents.
