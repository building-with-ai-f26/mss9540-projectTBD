# ResumeIQ

**Apply Easier.** Optimize your experience for every role without the hassle.

ResumeIQ is here to ensure your resume accurately reflects your experience for every job. Upload a PDF or Word `.docx` resume, or paste text, then add a specific job description to review strengths, missing evidence, and three suggested improvements. The primary user for PRD v1 is an NYU Stern MBA student recruiting for product management.

Build 1 due November 9, 2026 at noon, New York time. [PRD and build log](docs/index.html).

**Repository status:** The prototype, Product Page, screenshot, and project documents are included in the local implementation commit. GitHub publication requires pushing that commit. The private `.env` and virtual environment are excluded.

## Run locally

Python 3.8+ is required. In Terminal, install PDF support into a project virtual environment:

```bash
cd /Users/meherseera/Desktop/mss9540-projectTBD
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python server.py
```

Open http://127.0.0.1:8000 . Stop with Ctrl+C. If port 8000 is occupied, check whether ResumeIQ is already running in another terminal.

## Current interface

The local prototype uses a purple and lavender palette, a large “Apply Easier.” headline, soft background gradients, and two numbered input cards:

- **Your experience:** upload a PDF or Word document, or paste resume text. Extracted text appears in an editable preview.
- **Your next opportunity:** paste the specific job description.

Choose a review mode below the cards, then click **Analyze my resume**. Results appear in separate cards for **Strengths**, **Missing evidence**, and **Three next moves**. On smaller screens, the cards stack vertically.

The redesign changes presentation; the upload and analysis workflow is unchanged. Refresh the browser to load updated HTML and styling. The public Product Page at `docs/index.html` is a separate showcase with its own layout.

### Enable AI

The existing `.env` was a placeholder during implementation. Edit it privately in your editor. Do not paste credentials into chat, screenshots, browser code, or terminal output. If the file does not exist, copy `.env.example` to `.env`; never overwrite a real key with the example.

Set `OPENROUTER_API_KEY` to your actual key. Optionally set `OPENROUTER_MODEL` (default `openai/gpt-4o-mini`). Restart the server. Exported shell variables take precedence over `.env`.

Choose **AI analysis · OpenRouter**, load the fictional example, and analyze. A successful response is the actual connection check. The configuration indicator only checks for a non-placeholder key; credits, model availability, and networking may still prevent a review. Errors are displayed without silently substituting non-AI output.

AI mode sends both texts from the Python server to OpenRouter and its model provider. Remove personal details. This app has no database and does not save or log inputs; provider retention policies still apply. Credentials never go to the browser. The server is for local development only.

### Non-AI demo

Choose **Non-AI keyword comparison**, load the fictional example, and analyze. Literal shared/absent keywords and three generic prompts appear. This cannot interpret synonyms, assess qualifications, or establish resume quality. It calls no external API.

## Upload a resume

Choose a text-based PDF or Word `.docx` file, up to 5 MB (PDFs: 20 pages maximum). The local server extracts text in memory and fills the resume text box. Review and correct it before clicking Analyze. You can also paste text directly. Failed uploads preserve your existing text.

Scanned/image-only PDFs need OCR first. Password-protected PDFs and older `.doc` files are not supported; save as `.docx` or paste text. Complex layouts may extract in a different order. Word extraction covers body paragraphs and tables; headers, footers, and text boxes may need manual correction. Uploaded files are not saved or sent to OpenRouter; only the reviewed text is sent when you choose AI analysis.

After initial installation, start with `.venv/bin/python server.py`. Restart any previously running server to load the new upload endpoint.

Upload verification: ten automated tests passed, including real generated PDF/DOCX extraction, DOCX tables, invalid/encrypted/empty-text/oversized document rejection, and HTTP upload-to-non-AI-analysis for both formats. Tests use fictional generated documents, not user resumes. Try your own PDF and Word document and inspect the extracted text before the demo.

## Your two-minute demo and manual checks

1. Explain the primary user: a Stern MBA student tailoring a resume to a PM opening.
2. Load the fictional example, choose a mode, and analyze. State the mode honestly; use AI only after a successful live check.
3. Point out strengths, missing evidence, and exactly three improvements. Explain the edit you would make.
4. Try a blank field: the browser should prevent submission. Without a valid key, AI mode should show a setup error.
5. In AI mode, verify strengths cite real resume evidence, gaps reflect the job, and all three suggestions are actionable without invented facts. Try unrelated documents and documents with embedded instructions. These model quality checks are still pending.
6. Resize to phone width and navigate with the keyboard. Invite a reachable Stern student and record feedback only afterward.

## Checks completed

```bash
.venv/bin/python -m unittest discover -s tests -v
node --check app/app.js
```

The original five review tests and five new upload tests passed. Node is optional for the syntax check. Provider tests use simulated responses; these do not establish live AI quality.

After the redesign, headless Chrome verified the fictional-sample non-AI workflow and three suggestions, a 390px layout without horizontal overflow, 400 for invalid input, and 404 for private-file routes. A temporary desktop screenshot of the redesign was captured and visually inspected. JavaScript syntax and Git whitespace checks passed.

`docs/assets/prototype.png` is an actual screenshot of the earlier interface, before document uploads and the visual redesign. Its Product Page caption identifies it as an earlier version; it has not been replaced with the redesign preview.

Live AI response/quality, target-user usefulness, assistive technology, and public deployment remain unverified. Build 4 evaluation track is undecided. See [Plan.md](Plan.md).

## Publish after review

The builder authorized committing the project files locally. Add actual personal hours, costs, and learning to the Product Page before submission. Pushing the implementation to GitHub remains a separate step. When ready, stage only reviewed files, confirm `.env` is ignored (`git check-ignore .env`) and absent from staged changes, then commit and push approved changes to `main`.

On GitHub:

1. Ensure the repository is public for the assignment.
2. Open **Settings → Pages**.
3. Under **Build and deployment**, select **Deploy from a branch**.
4. Choose **main**, **/docs**, then **Save**.
5. Wait for deployment; follow GitHub’s published-site link. Verify the PRD, log, and screenshot in a private browser window.

Expected address for this repository: https://building-with-ai-f26.github.io/mss9540-projectTBD/ . Publication has not been verified. GitHub Pages hosts the showcase, not the local Python app.

Reference: [GitHub Pages publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

Submit the published Product Page and [repository URL](https://github.com/building-with-ai-f26/mss9540-projectTBD) in Icerynk. The class template requires meaningful commits on two separate days outside class; do not invent or backdate history.

## Main files

- `server.py`: server, environment configuration, OpenRouter, validation, keyword fallback.
- `resume_files.py`: in-memory PDF and Word text extraction; `requirements.txt`: pinned PDF dependency.
- `app/`: browser interface.
- `tests/test_server.py`: deterministic behavior and simulated provider tests.
- `tests/test_uploads.py`: document extraction and HTTP upload-to-analysis checks.
- `docs/index.html`, `docs/assets/prototype.png`: PRD, build log, actual screenshot.
- `AGENTS.md`, `Intent.md`, `Plan.md`: rules, intent, architecture and risks.

API reference: [OpenRouter chat completions](https://openrouter.ai/docs/api/api-reference/chat/send-chat-completion-request).
