# ?? Verity — Autonomous AI QA Engineer Studio

> **Precision Test Architecture from Stories, Specs & Wireframes**

Verity is an **autonomous, multimodal AI-powered QA engineering platform** built on Google ADK and Gemini multimodal vision. It deeply analyzes user stories, requirements PDFs, and UI wireframe images together — synthesizing every input — to generate an exhaustive, fully traceable, production-ready test plan exported as a richly formatted PDF, Excel workbook, JSON, CSV, or interactive SVG diagram.

---

## ? Key Features

| Capability | Description |
|---|---|
| ?? **Autonomous AI QA Agent (Verity)** | Named Verity, powered by Google ADK + Gemini multimodal, acts as a senior QA engineer |
| ??? **Multimodal Wireframe Analysis** | Sends UI wireframes/screenshots to Gemini Vision; maps visible UI controls, states, and journeys |
| ?? **PDF Requirement Ingestion** | Extracts text from requirement PDFs (pypdf) and feeds it into Verity's planning context |
| ?? **User Story & Acceptance Criteria Parsing** | Interprets free-form user stories and business rules into traceable requirements |
| ?? **Elaborately Described PDF Export** | Generates production-grade A4 PDF with visual flow, metrics dashboard, traceability matrix, and per-case cards |
| ?? **Visual Flow Diagram (PDF-embedded)** | Vector diagram inside PDF: Source Ingestion ? Verity AI Engine ? Test Architecture ? Verification Plan |
| ?? **Requirements Traceability Matrix** | Every test case cross-referenced to its source requirement with confidence and coverage status |
| ?? **Structured Test Case Cards** | Each case includes objective, preconditions, numbered steps, expected result, test data, and automation flag |
| ?? **Multi-format Export** | PDF Report, Excel Workbook, JSON, CSV, SVG workflow diagram |
| ?? **Coverage Mode Selection** | Choose UI only, API only, or combined UI + API test coverage per generation run |
| ?? **Streamlit Web UI** | Polished dark-themed dashboard, fully interactive; no database required |

---

## ??? Architecture Overview

```
+-------------------------------------------------------------+
¦                   Verity Studio (Streamlit UI)               ¦
¦            app/main.py — Wide layout dashboard               ¦
+-------------------------------------------------------------+
                                ¦
              +-----------------?------------------+
              ¦        Input Ingestion Layer         ¦
              ¦  User Story ¦ PDF Text ¦ Wireframes  ¦
              ¦      app/services/input_service.py   ¦
              +------------------------------------+
                                ¦
              +-----------------?------------------+
              ¦       ADK Orchestration Layer        ¦
              ¦      app/services/adk_planner.py     ¦
              ¦  InMemoryRunner + Session Management  ¦
              +------------------------------------+
                                ¦
              +-----------------?------------------+
              ¦     Verity — Google ADK Agent        ¦
              ¦       qa_agent/agent.py              ¦
              ¦  Model: gemini-3.8-flash (Vision)    ¦
              ¦  Instruction: Elite QA Specialist    ¦
              +------------------------------------+
                                ¦
              +-----------------?------------------+
              ¦       Output & Export Layer          ¦
              ¦   app/services/Report_services.py    ¦
              ¦  PDF ¦ XLSX ¦ JSON ¦ CSV ¦ SVG       ¦
              +------------------------------------+
```

---

## ?? Project Structure

```
QAEngineer/
+-- main.py                          # Entry point — auto-detects venv & launches Streamlit
+-- .env                             # API keys and model config (not committed)
+-- requirements.txt                 # All Python dependencies
+-- README.md                        # This file
¦
+-- app/
¦   +-- main.py                      # Streamlit dashboard (1000+ lines, full UI)
¦   +-- config.py                    # Config proxy (re-exports from core)
¦   +-- core/
¦   ¦   +-- config.py                # APP_NAME, APP_TAGLINE, API keys, model selection
¦   +-- models/
¦   ¦   +-- schemas.py               # Pydantic models: TestPlan, TestCase, Requirement
¦   +-- services/
¦   ¦   +-- adk_planner.py           # ADK InMemoryRunner + Verity orchestration
¦   ¦   +-- input_service.py         # Proxy for input_services
¦   ¦   +-- input_services.py        # PDF text extraction, image loading
¦   ¦   +-- report_service.py        # Proxy for Report_services
¦   ¦   +-- Report_services.py       # PDF, XLSX, CSV, JSON, SVG generators
¦   +-- agents/                      # ADK agent extensions (reserved)
¦   +-- api/                         # FastAPI endpoints (reserved)
¦   +-- integrations/                # Third-party integrations (reserved)
¦   +-- tools/                       # ADK tool definitions (reserved)
¦
+-- qa_agent/
¦   +-- agent.py                     # Verity root_agent definition + instruction prompt
¦   +-- .env                         # Agent-scoped env override
¦
+-- config/
¦   +-- config.py                    # Project-level config proxy
¦
+-- tests/
    +-- test_smoke.py                # Smoke tests: imports, config, schema, reporting
```

---

## ?? Getting Started

### Prerequisites

- **Python 3.10+** (3.13 recommended)
- **Google Gemini API Key** — get one at [aistudio.google.com](https://aistudio.google.com/)

### 1. Clone & Set Up Virtual Environment

```powershell
# Create a shared virtual environment (recommended alongside other projects)
python -m venv AgentsVenv
.\AgentsVenv\Scripts\Activate.ps1

# Install all dependencies
pip install -r QAEngineer\requirements.txt
```

### 2. Configure API Key

Create or edit `QAEngineer/.env`:

```env
GOOGLE_API_KEY="your_gemini_api_key_here"
GOOGLE_MODEL="gemini-3.8-flash"
```

### 3. Launch Verity Studio

```powershell
# Option A — auto-launcher (recommended, finds the venv automatically)
python QAEngineer\main.py

# Option B — direct Streamlit launch (with venv activated)
streamlit run QAEngineer\app\main.py

# Option C — using the venv python explicitly
C:\AgenticProjects\AgentsVenv\Scripts\python.exe -m streamlit run QAEngineer\app\main.py
```

Then open **http://localhost:8501** in your browser.

---

## ?? How Verity Works

### 1. You Provide the Source Material
- **User Story / Acceptance Criteria** — paste freeform text describing what the software should do
- **Requirements PDF** — upload a `.pdf` document; text is extracted automatically
- **UI Wireframes / Screenshots** — upload `.png`, `.jpg`, or `.webp` images; sent to Gemini Vision

### 2. Verity Analyzes Everything
Verity's instruction prompt guides it to:
- Identify **all visible UI elements** in wireframe images (fields, buttons, dropdowns, states)
- **Separate stated requirements** from inferred behaviors and wireframe-only observations
- **Never invent API contracts**, endpoints, or authentication mechanisms
- Produce **high-confidence test cases** with realistic preconditions, test data, and verifiable expected results

### 3. You Get a Complete Test Plan
Verity outputs a structured JSON plan (validated via Pydantic) containing:

| Field | Description |
|---|---|
| `plan_title` | Auto-generated descriptive title |
| `version` | Plan version string |
| `summary` | Executive summary |
| `scope_in` / `scope_out` | Clear test scope boundaries |
| `requirements[]` | Traced requirements with source and confidence |
| `test_cases[]` | Full test case cards (see below) |
| `assumptions[]` | Engineering assumptions made |
| `open_questions[]` | Gaps to resolve before execution |
| `source_notes[]` | Notes on what was analyzed |

Each **TestCase** includes:
```
test_case_id · title · layer (UI/API/UI+API) · test_type
priority (P0-P3) · requirement_id · objective
preconditions · test_data · steps · expected_result
assumptions · automation_candidate
```

---

## ?? PDF Report — What's Inside

The exported PDF (`ai_qa_test_plan.pdf`) is professionally structured:

```
+---------------------------------------------------------+
¦  VERITY • AUTONOMOUS MULTIMODAL AI QA ENGINEER           ¦
¦  Precision Test Architecture from Stories, Specs & Frames¦
¦  [Plan Title]                    Version | Author | Status¦
¦  [Executive Summary]                                     ¦
+---------------------------------------------------------¦
¦  METRICS DASHBOARD                                       ¦
¦  Total Cases ¦ UI Coverage ¦ API Coverage ¦ Reqs ¦ Auto% ¦
+---------------------------------------------------------¦
¦  1. TEST SCOPE & BOUNDARIES                              ¦
¦  In Scope --------------- ¦ Out of Scope -------------- ¦
+---------------------------------------------------------¦
¦  2. VISUAL COVERAGE FLOW (Embedded Vector Diagram)       ¦
¦  [Source Ingestion] ? [Verity AI] ? [Test Architecture]  ¦
¦              ? [Verification Plan]                       ¦
+---------------------------------------------------------¦
¦  3. REQUIREMENTS TRACEABILITY MATRIX                     ¦
¦  ID ¦ Statement ¦ Source ¦ Confidence ¦ Traced Test Cases ¦
+---------------------------------------------------------¦
¦  4. ELABORATELY DESCRIBED TEST CASES                     ¦
¦  +-- TC-001: [Title]         P0 - Critical ¦ UI         +¦
¦  ¦ Req: REQ-001 ¦ Type: Functional ¦ ? Automation       ¦¦
¦  ¦ Objective: …                                          ¦¦
¦  ¦ Preconditions: … ¦ Test Data: …                       ¦¦
¦  ¦ Step 1: … / Step 2: … / Step 3: …                    ¦¦
¦  ¦ Expected Result: …                                    ¦¦
¦  +------------------------------------------------------ +¦
+---------------------------------------------------------¦
¦  5. ARCHITECTURAL ASSUMPTIONS & OPEN QUESTIONS           ¦
¦  Assumptions: … ¦ Open Questions & Gaps: …               ¦
+---------------------------------------------------------+
Footer: Verity — Autonomous AI QA Engineer Studio • Joshu Joseph     Page N
```

---

## ?? Export Formats

| Format | File | Contents |
|---|---|---|
| **?? PDF Report** | `ai_qa_test_plan.pdf` | Full report with visual flow, cards, traceability |
| **?? Excel Workbook** | `ai_qa_test_plan.xlsx` | Test cases in spreadsheet with styling |
| **?? JSON** | `ai_qa_test_plan.json` | Machine-readable full plan (Pydantic model) |
| **?? CSV** | `ai_qa_test_cases.csv` | Flat test case rows for import to Jira/TestRail |
| **??? SVG Diagram** | `test_planning_workflow.svg` | Visual workflow diagram |

---

## ?? Technology Stack

| Layer | Technology |
|---|---|
| **AI Agent** | Google ADK (`google-adk`) |
| **Multimodal Vision** | Google Gemini (`gemini-3.8-flash`) via `google-genai` |
| **Web UI** | Streamlit |
| **PDF Generation** | ReportLab (platypus + graphics shapes) |
| **Excel Export** | openpyxl |
| **PDF Parsing** | pypdf |
| **Data Validation** | Pydantic v2 |
| **Configuration** | python-dotenv |
| **Testing** | pytest + pytest-asyncio |
| **Code Quality** | ruff |

---

## ?? Supported Test Types

Verity generates test cases across all standard QA disciplines:

- **Functional** — core business logic validation
- **Negative** — invalid inputs, failure paths
- **Boundary** — edge values, limits
- **Validation** — form validation, input constraints
- **Accessibility** — a11y considerations from visible UI
- **Usability** — UX flow completeness
- **Integration** — cross-system interaction points
- **Security** — authentication, authorization, data exposure
- **Compatibility** — cross-browser/device considerations
- **Error Handling** — system behavior under failure conditions

### Priority Levels

| Priority | Description |
|---|---|
| P0 - Critical | System cannot function; must pass for release |
| P1 - High | Core user journeys; high business impact |
| P2 - Medium | Important features; moderate risk if failing |
| P3 - Low | Nice-to-have; low impact edge cases |

---

## ?? Running Tests

```powershell
# Activate virtual environment first
.\AgentsVenv\Scripts\Activate.ps1

# Run smoke tests
python -m pytest QAEngineer\tests\ -v

# Expected output:
# tests\test_smoke.py::test_config PASSED
# tests\test_smoke.py::test_schema_and_reporting PASSED
# 2 passed in ~1s
```

---

## ?? Configuration Reference

| Variable | Default | Description |
|---|---|---|
| `GOOGLE_API_KEY` | *(required)* | Your Gemini API key from Google AI Studio |
| `GOOGLE_MODEL` | `gemini-3.8-flash` | Gemini model to use (must support vision) |

Set in `QAEngineer/.env` or `QAEngineer/qa_agent/.env`.

---

## ??? Roadmap

- [ ] Jira / TestRail integration for direct test case import
- [ ] FastAPI backend for headless plan generation via REST API
- [ ] Playwright-powered UI validation automation export
- [ ] VAPT (vulnerability assessment) test coverage via bandit + semgrep integration
- [ ] OpenAPI / Swagger spec ingestion for automatic API test generation
- [ ] Multi-agent orchestration (Planner agent + Reviewer agent + Formatter agent)
- [ ] Historical plan versioning and diff comparison

---

## ????? Author

**Joshu Joseph** — AI Engineer & Full-Stack Developer

Building autonomous AI systems that bridge engineering rigor with developer experience.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0a66c2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/joshu-joseph-374a101bb)

---

## ?? License

This project is private and proprietary to Joshu Joseph.

---

*Verity — Precision Test Architecture from Stories, Specs & Wireframes*
