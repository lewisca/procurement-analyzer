# Procurement Analyzer

Buyer-side due-diligence prototype for **agentic AI vendors**. Drop a
folder of vendor artifacts (overview, tool schema, sample trace, failure-mode
doc, etc.) and get back a structured markdown report with 1–5 scores
against a 15-question rubric.

## Rubric

Three risk categories that are unique to agentic AI:

1. **Tool-Call Correctness** — does the agent invoke tools safely?
2. **Loop Termination / Step Budgets** — can it spiral or burn through budgets?
3. **Multi-Step State Coherence** — does it stay consistent over long runs?

Five questions per category; scored 1–5. See [rubric/horizontal_v1.yaml](rubric/horizontal_v1.yaml).

A maternal-health / clinical-AI extension is sketched in the same file
under `extensions`. Layered scoring is not implemented in v1.

## Quickstart

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

### Web UI (recommended)

```bash
python -m web.app
# or:  flask --app web/app.py run
```

Visit http://127.0.0.1:5000. The page reads the artifact taxonomy at
startup and renders one upload slot per artifact type. Required slots
are grouped first; optional below. After submit, the analyzer runs
(~30–60 s) and you get the report inline with a "Download markdown"
button.

### CLI (for batch / scripted use)

```bash
python -m analyzer vendors/lumen-agents
python -m analyzer vendors/quickbot-ai
```

Reports land in `reports/`. Add `--json out.json` to also dump the raw
structured result.

## Project layout

```
.
├── rubric/horizontal_v1.yaml      The rubric (edit me — no code change required)
├── vendors/                       Drop a folder per vendor here
│   ├── lumen-agents/              Mock: mature vendor (mostly optimal answers)
│   └── quickbot-ai/               Mock: early-stage vendor (lots of red flags)
├── analyzer/                      The analyzer package
│   ├── rubric.py                  YAML loader for the rubric
│   ├── artifacts.py               YAML loader + slot matching for the taxonomy
│   ├── analyzer.py                Calls Claude, returns structured result
│   ├── report.py                  Markdown renderer
│   └── __main__.py                CLI
├── web/                           Flask UI
│   ├── app.py                     Routes: GET / and POST /analyze
│   ├── templates/                 index, report, error
│   └── static/style.css           Retro stylesheet
└── reports/                       Generated reports (gitignored in real use)
```

## How it works

1. Reads every supported file (`.md`, `.json`, `.yaml`, `.txt`) in the
   vendor folder.
2. Builds one Claude call containing the rubric + every artifact.
3. Forces a tool-use response so the output is strict structured JSON
   (one score, one confidence, evidence quotes, reasoning, and gaps per
   question, plus an overall observations field).
4. Renders the JSON as a markdown report with a verdict, per-category
   scorecard, and per-question evidence trail.

## Adding a vendor

Drop a new folder under `vendors/` with whatever artifacts you have.
The analyzer doesn't require any specific filenames — it just reads
everything supported. Useful artifacts to look for:

- Product / overview docs
- Tool / function schemas
- Sample execution traces or logs
- Failure-mode or reliability docs
- Security & privacy documentation
- Evaluation / benchmark reports
- Pricing, SLA, and contract terms

## Artifact taxonomy (UI contract)

The list of artifacts a buyer should request from a vendor lives in
[rubric/artifact_taxonomy.yaml](rubric/artifact_taxonomy.yaml). It's the
source of truth for two things:

1. **The analyzer** — accepted file suffixes, slot matching, coverage.
2. **The future UI** — upload slots with `name`, `description`,
   `ask_vendor` copy, and `example_filenames`.

If you add a new slot in the YAML, both the analyzer and the UI pick it
up without code changes (UI just iterates `slots`; analyzer reads
`accepted_suffixes` on load).

## What the analyzer reads

| Format                       | Behavior                                          |
|------------------------------|---------------------------------------------------|
| `.md / .json / .yaml / .txt` | Read as plain text                                |
| `.ndjson / .mmd`             | Read as plain text                                |
| `.py / .ts / .js / .go / .rb`| Read as plain text (good for tool / loop code)    |
| `.pdf`                       | Text-extracted via `pypdf` (no OCR for scans)     |
| `.png / .svg / .jpg`         | Skipped with a note — user reviews separately     |
| `.docx / .pptx`              | Not yet supported                                 |
| `~$*`, dotfiles              | Skipped (Office lock files, temp junk)            |

## Status

This is a working prototype. Known limitations:

- Single Claude call; doesn't yet batch by category for long artifact sets.
- No prompt caching — every run re-pays the input tokens.
- Scanned PDFs (image-only, no text layer) aren't OCR'd.
- `.docx` and `.pptx` are not yet supported.
- The vertical extension hooks in the rubric are documented but not
  scored.
