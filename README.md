# VERIQ AI — Autonomous AI QA Engineer Studio

> **Precision test architecture from stories, specifications, and wireframes.**

VERIQ AI is an autonomous, multimodal AI-powered quality assurance platform built with Google ADK and Gemini vision. It analyzes user stories, requirements PDFs, and UI wireframes to generate structured, traceable test plans for software teams.

## Table of contents

- [Features](#features)
- [Architecture](#architecture)
- [Project structure](#project-structure)
- [Getting started](#getting-started)
- [How it works](#how-it-works)
- [PDF report contents](#pdf-report-contents)
- [Export formats](#export-formats)
- [Technology stack](#technology-stack)
- [Supported test types](#supported-test-types)
- [Running tests](#running-tests)
- [Configuration](#configuration)
- [Roadmap](#roadmap)
- [Author](#author)
- [License](#license)

## Features

| Capability | Description |
|---|---|
| **Autonomous AI QA agent** | Uses Google ADK and Gemini multimodal capabilities to plan tests like a QA engineer. |
| **Wireframe and screenshot analysis** | Identifies visible UI controls, states, and user journeys from images. |
| **PDF requirement ingestion** | Extracts text from requirement PDFs and adds it to the planning context. |
| **User story and acceptance criteria parsing** | Turns free-form stories and business rules into traceable requirements. |
| **Structured test cases** | Produces test objectives, preconditions, numbered steps, expected results, test data, and automation candidacy. |
| **Requirements traceability** | Links test cases to source requirements with confidence and coverage information. |
| **PDF report generation** | Creates an A4 report with a visual flow, metrics dashboard, traceability matrix, and test case cards. |
| **Multiple export formats** | Exports plans as PDF, Excel, JSON, CSV, and SVG. |
| **Coverage mode selection** | Selects UI, API, or combined UI and API coverage for a generation run. |
| **Streamlit web UI** | Provides an interactive dashboard; no database is required. |

## Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│                    VERIQ AI Studio (Streamlit)                │
│                    app/main.py — dashboard                    │
└────────────────────────────┬─────────────────────────────────┘
                             │
              ┌──────────────▼───────────────┐
              │       Input ingestion        │
              │ User stories, PDFs, images   │
              │ app/services/input_services.py│
              └──────────────┬───────────────┘
                             │
              ┌──────────────▼───────────────┐
              │      ADK orchestration       │
              │ app/services/adk_planner.py  │
              │ InMemoryRunner + sessions    │
              └──────────────┬───────────────┘
                             │
              ┌──────────────▼───────────────┐
              │      VERIQ AI QA agent       │
              │ qa_agent/agent.py            │
              │ Google ADK + Gemini vision   │
              └──────────────┬───────────────┘
                             │
              ┌──────────────▼───────────────┐
              │       Output and export      │
              │ app/services/Report_services.py│
              │ PDF, XLSX, JSON, CSV, SVG    │
              └──────────────────────────────┘
```

## Project structure

```text
VERIQ-AI/
├── main.py                         # Entry point; launches Streamlit
├── .env                            # API keys and model config (not committed)
├── requirements.txt                # Python dependencies
├── README.md
├── app/
│   ├── main.py                     # Streamlit dashboard
│   ├── config.py                   # Config proxy
│   ├── core/
│   │   └── config.py               # App name, tagline, keys, model selection
│   ├── models/
│   │   └── schemas.py              # Pydantic test plan, case, and requirement models
│   ├── services/
│   │   ├── adk_planner.py          # ADK runner and VERIQ AI orchestration
│   │   ├── input_service.py        # Input service proxy
│   │   ├── input_services.py       # PDF text extraction and image loading
│   │   ├── report_service.py       # Report service proxy
│   │   └── Report_services.py      # PDF, XLSX, CSV, JSON, and SVG generators
│   ├── agents/                     # Reserved for ADK agent extensions
│   ├── api/                        # Reserved for FastAPI endpoints
│   ├── integrations/               # Reserved for third-party integrations
│   └── tools/                      # Reserved for ADK tool definitions
├── qa_agent/
│   ├── agent.py                    # VERIQ AI root agent and instruction prompt
│   └── .env                        # Agent-scoped environment overrides
├── config/
│   └── config.py                   # Project-level config proxy
└── tests/
    └── test_smoke.py               # Smoke tests for imports, config, schemas, and reports
```

## Getting started

### Prerequisites

- Python 3.10 or later (Python 3.13 is recommended)
- A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/)

### 1. Create and activate a virtual environment

From the project directory, run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure your API key

Create a `.env` file in the project root and add your Google API key and preferred model:

```env
GOOGLE_API_KEY="your_gemini_api_key_here"
GOOGLE_MODEL="gemini-3.8-flash"
```

Keep `.env` files and API keys private; do not commit secrets to the repository.

### 3. Launch VERIQ AI

From the project directory, run either:

```powershell
# Project launcher
python main.py

# Or launch Streamlit directly
streamlit run app\main.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

## How it works

### 1. Provide source material

- **User stories and acceptance criteria:** Paste the text describing expected behavior.
- **Requirements PDF:** Upload a `.pdf` file; its text is extracted automatically.
- **Wireframes and screenshots:** Upload `.png`, `.jpg`, or `.webp` images for Gemini vision analysis.

### 2. VERIQ AI analyzes the inputs

The agent is instructed to:

- Identify visible UI elements, such as fields, buttons, dropdowns, and states.
- Distinguish stated requirements from inferred behavior and observations from wireframes.
- Avoid inventing API contracts, endpoints, or authentication mechanisms.
- Generate high-confidence test cases with realistic preconditions, test data, and verifiable expected results.

### 3. Review the generated test plan

VERIQ AI produces a structured JSON plan validated with Pydantic. It includes:

| Field | Description |
|---|---|
| `plan_title` | Automatically generated descriptive title |
| `version` | Plan version string |
| `summary` | Executive summary |
| `scope_in` / `scope_out` | In-scope and out-of-scope boundaries |
| `requirements[]` | Requirements with source and confidence information |
| `test_cases[]` | Structured test case cards |
| `assumptions[]` | Engineering assumptions made during planning |
| `open_questions[]` | Gaps to resolve before execution |
| `source_notes[]` | Notes about the analyzed inputs |

Each test case includes an ID, title, layer (UI/API/UI+API), test type, priority, linked requirement, objective, preconditions, test data, steps, expected result, assumptions, and automation candidacy.

## PDF report contents

The generated `ai_qa_test_plan.pdf` report includes:

1. **Cover and summary** — plan title, version, author, status, and executive summary.
2. **Metrics dashboard** — total cases, UI and API coverage, requirements, and automation percentage.
3. **Test scope and boundaries** — in-scope and out-of-scope items.
4. **Visual coverage flow** — source ingestion through VERIQ AI analysis to the verification plan.
5. **Requirements traceability matrix** — requirement statements, sources, confidence, and linked test cases.
6. **Test case cards** — priority, type, objective, preconditions, test data, steps, and expected result.
7. **Assumptions and open questions** — planning assumptions and unresolved gaps.

## Export formats

| Format | Output file | Contents |
|---|---|---|
| PDF report | `ai_qa_test_plan.pdf` | Full report with visual flow, test case cards, and traceability |
| Excel workbook | `ai_qa_test_plan.xlsx` | Styled test cases in a spreadsheet |
| JSON | `ai_qa_test_plan.json` | Machine-readable plan validated by Pydantic |
| CSV | `ai_qa_test_cases.csv` | Flat test case rows for tools such as Jira or TestRail |
| SVG diagram | `test_planning_workflow.svg` | Visual workflow diagram |

## Technology stack

| Layer | Technology |
|---|---|
| AI agent | Google ADK (`google-adk`) |
| Multimodal vision | Google Gemini (`gemini-3.8-flash`) via `google-genai` |
| Web UI | Streamlit |
| PDF generation | ReportLab |
| Excel export | openpyxl |
| PDF parsing | pypdf |
| Data validation | Pydantic v2 |
| Configuration | python-dotenv |
| Testing | pytest and pytest-asyncio |
| Code quality | ruff |

## Supported test types

VERIQ AI can generate test cases across common QA disciplines:

- **Functional** — core business logic
- **Negative** — invalid inputs and failure paths
- **Boundary** — edge values and limits
- **Validation** — form validation and input constraints
- **Accessibility** — accessibility considerations from visible UI
- **Usability** — completeness of user experience flows
- **Integration** — cross-system interaction points
- **Security** — authentication, authorization, and data exposure
- **Compatibility** — cross-browser and device considerations
- **Error handling** — behavior under failure conditions

### Priority levels

| Priority | Description |
|---|---|
| P0 — Critical | The system cannot function; must pass for release. |
| P1 — High | Core user journeys with high business impact. |
| P2 — Medium | Important features with moderate risk if they fail. |
| P3 — Low | Nice-to-have features and low-impact edge cases. |

## Running tests

Activate your virtual environment, then run the test suite from the project directory:

```powershell
python -m pytest tests\ -v
```

The repository currently documents smoke tests for configuration, schemas, and reporting.

## Configuration

| Variable | Default | Description |
|---|---|---|
| `GOOGLE_API_KEY` | Required | Google Gemini API key from Google AI Studio |
| `GOOGLE_MODEL` | `gemini-3.8-flash` | Gemini model to use; it must support vision |

Set these values in the project root `.env` or, if needed, in `qa_agent/.env`.

## Roadmap

- [ ] Jira and TestRail integration for direct test case import
- [ ] FastAPI backend for headless plan generation
- [ ] Playwright-powered UI validation automation export
- [ ] VAPT test coverage through Bandit and Semgrep integration
- [ ] OpenAPI/Swagger specification ingestion for API test generation
- [ ] Multi-agent orchestration (planner, reviewer, and formatter agents)
- [ ] Historical plan versioning and diff comparison

## Author

**Joshu Joseph** — AI Engineer and Full-Stack Developer

Building autonomous AI systems that bridge engineering rigor with developer experience.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0a66c2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/joshu-joseph-374a101bb)

## License

This project is private and proprietary to Joshu Joseph.

---

*VERIQ AI — Precision test architecture from stories, specifications, and wireframes.*
