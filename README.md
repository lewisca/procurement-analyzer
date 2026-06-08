# Procurement Analyzer

**Procurement-grade evaluation for agentic AI vendors.** Drop a folder of
public vendor docs, get back a structured report with 1–5 scores against
a 15-question rubric covering tool-call correctness, loop termination,
and multi-step state coherence — the three risk categories unique to
agentic AI.

---

## A 5-vendor comparison this tool produced

| Vendor | Tool-Call | Loop Term. | State Coh. | **Weighted** |
|--------|----------:|-----------:|-----------:|-------------:|
| Anthropic Claude Agent SDK | 4.00 | 2.80 | 3.00 | **3.27** |
| OpenAI Agents SDK | 3.60 | 3.20 | 2.80 | **3.20** |
| LangGraph | 2.60 | 2.60 | 2.80 | **2.67** |
| Sierra | 2.60 | 2.80 | 2.00 | **2.47** |
| Salesforce Agentforce | 2.60 | 2.20 | 2.00 | **2.27** |

Sample reports for each are in [`examples/`](examples/). The methodology
is fully documented in [`rubric/horizontal_v1.yaml`](rubric/horizontal_v1.yaml).

**Counterintuitive finding:** Salesforce Agentforce came last despite
having the broadest enterprise compliance footprint (SOC 2, ISO 27001,
PCI-DSS, HIPAA, FedRAMP, GDPR). The rubric penalized lack of public
quantitative evidence and lack of buyer-visible step / cost ceilings.
Public documentation depth correlates with procurement-readiness more
than compliance breadth does. *Show your work isn't a bias — it's a
requirement.*

## What this is

A buyer-side procurement tool for vendors of agentic AI products. It
answers a specific question: *given what's publicly documented, can a
procurement team verify the vendor's claims about agent safety, loop
termination, and state coherence?*

Three risk categories, five questions each, scored 1–5:

1. **Tool-Call Correctness** — does the agent invoke tools safely?
2. **Loop Termination / Step Budgets** — can it spiral or burn through budgets?
3. **Multi-Step State Coherence** — does it stay consistent over long runs?

## What this is NOT

A complete procurement decision. The rubric scores **one dimension**:
how procurement-ready a vendor's public posture is. It does **not** tell
you:

- Whether the vendor's category matches your business need
- Time-to-value (managed product vs framework — 6 weeks vs 6 months)
- Team capability fit (Python developers vs Salesforce admins)
- Integration depth with your existing systems
- Total cost of ownership at scale
- Vertical certifications (FedRAMP, FDA SaMD, FINRA)

A sound procurement decision is three layers — **business-fit screen →
category selection → vendor due diligence within category**. This tool
addresses the third layer. Use it to pick *within* a category (Sierra vs
Decagon vs Cresta; or Anthropic vs OpenAI) — not *across* fundamentally
different categories.

Every report includes a "Scope of this evaluation" section spelling this
out.

## Quickstart

```bash
git clone https://github.com/lewisca/procurement-analyzer.git
cd procurement-analyzer
pip install -r requirements.txt
```

Create a `.env` file with your Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-api03-...
```

### Web UI (recommended)

```bash
python -m web.app
```

Open <http://127.0.0.1:5000>. Upload all of a vendor's docs at once via
the "Quick upload" card, name the vendor, click **Analyze vendor**.
Analysis takes 30–60 seconds. The report renders inline with a verdict,
an executive summary, score chips, per-question evidence quotes, and a
markdown download.

### CLI

```bash
python -m analyzer vendors/anthropic-claude
python -m analyzer vendors/sierra --json reports/sierra.json
```

Reports land in `reports/`; raw structured results in `runs/`.

### Compare two vendors

After running two analyses, visit `/compare` in the web UI, pick two
saved runs, get a side-by-side report.

## Adding a vendor

Drop a folder under `vendors/<vendor-name>/` with whatever public docs
you have. The taxonomy in
[`rubric/artifact_taxonomy.yaml`](rubric/artifact_taxonomy.yaml)
defines 14 artifact slots — what to ask for, what format, what an
example looks like. **Be honest about gaps**: if a vendor doesn't
publish their failure-mode rates, the file should say so. The
analyzer's gap-detection only works if files honestly mark what's
missing.

The existing folders in [`vendors/`](vendors/) — anthropic-claude,
openai-agents, sierra, salesforce-agentforce, langgraph — are real
reference vendors you can study to see the pattern.

## How it works

1. Reads every supported file (`.md`, `.json`, `.yaml`, `.py`, `.mmd`,
   `.pdf`, etc.) in the vendor folder.
2. Matches each file to one of 14 artifact slots by filename heuristics.
3. Sends the rubric + every artifact to Claude in one call, forcing a
   tool-use response so output is strict structured JSON (one score,
   confidence, evidence quotes, reasoning, and gaps per question).
4. Renders as a markdown report with executive summary, scope section,
   per-category scorecard, per-question evidence trail, and a
   "what to do next" agenda for the buyer.

The 15-question rubric and the 14-slot artifact taxonomy are both
YAML — edit them without touching code.

## What the analyzer reads

| Format | Behavior |
|--------|----------|
| `.md / .json / .yaml / .txt / .ndjson / .mmd` | Read as plain text |
| `.py / .ts / .js / .go / .rb` | Read as plain text (good for code) |
| `.pdf` | Text-extracted via `pypdf` (no OCR for scans) |
| `.png / .svg / .jpg` | Skipped — review images separately |
| `.docx / .pptx` | Not yet supported |
| Office lock files, dotfiles | Skipped |

## Project layout

```
.
├── rubric/
│   ├── horizontal_v1.yaml        15-question rubric (editable, no code change)
│   └── artifact_taxonomy.yaml    14-slot artifact taxonomy
├── vendors/                      One folder per vendor
│   ├── anthropic-claude/         Real reference (3.27 / 5)
│   ├── openai-agents/            Real reference (3.20 / 5)
│   ├── langgraph/                Real reference (2.67 / 5)
│   ├── sierra/                   Real reference (2.47 / 5)
│   ├── salesforce-agentforce/    Real reference (2.27 / 5)
│   ├── lumen-agents/             Mock "mature" vendor (5.0 / 5)
│   └── quickbot-ai/              Mock "early stage" vendor (1.0 / 5)
├── analyzer/                     Python package
│   ├── rubric.py                 YAML loader
│   ├── artifacts.py              YAML loader + slot matching
│   ├── analyzer.py               Claude call + structured output
│   ├── compare.py                Side-by-side comparison logic
│   ├── report.py                 Markdown renderer
│   ├── env_loader.py             .env support
│   └── __main__.py               CLI
├── web/                          Flask UI (SaaS-style dashboard)
│   ├── app.py                    Routes
│   ├── templates/                Jinja templates
│   └── static/style.css          Design system
└── examples/                     Sample reports (so you can see output without running)
```

## Status and known limitations

Working prototype, used to evaluate the five real vendors shown in the
scorecard. Known limitations to be honest about:

- Single Claude call per vendor; doesn't yet batch by category.
- No prompt caching — every run re-pays input tokens.
- Scanned PDFs (image-only) aren't OCR'd.
- `.docx` and `.pptx` not yet supported.
- Vertical extensions in the rubric (maternal health, etc.) are
  documented but not scored.
- No multi-vendor comparison beyond pairwise. A "Gartner-style"
  N-vendor leaderboard exists in `examples/` but isn't a built-in view.

## Contributing

Three high-leverage contribution paths if you want to help:

1. **New rubric questions.** Edit
   [`rubric/horizontal_v1.yaml`](rubric/horizontal_v1.yaml) and submit
   a PR with your reasoning. Questions should be answerable from public
   docs.
2. **New reference vendors.** Drop a `vendors/<name>/` folder following
   the existing pattern. Verticals (healthcare, legal, voice) are
   especially welcome.
3. **Methodology critique.** Open an issue. "Your rubric is unfair to
   [vendor X] because…" is exactly the kind of feedback that improves
   the tool.

## License

[MIT](LICENSE). Use freely, commercially or otherwise.

## About

Built by [Chris Lewis](https://github.com/lewisca). Background in
procurement / IT leadership; this is the tool I wished existed when
evaluating agentic AI vendors for real procurement decisions.

The rubric is derived from a published agentic-AI evaluation framework;
the analyzer was built to make that framework executable against any
vendor's public docs.
