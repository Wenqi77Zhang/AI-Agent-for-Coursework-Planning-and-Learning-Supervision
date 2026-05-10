# AssignmentPilot

AssignmentPilot is an Agentic AI demo project for the `CA6123 Agentic AI and Applications` course.
It follows a `Perceive -> Context -> Reason -> Action -> Learn` workflow to parse assignment briefs, generate a team plan, and export submission-ready artifacts.

## Features

- `Perceive`: Reads the assignment brief and extracts structured requirements with an LLM.
- `Context`: Infers or accepts team size and available development days.
- `Reason`: Classifies user intent, then produces architecture/planning outputs, task breakdowns, and team allocation.
- `Action`: Executes tool calls and writes Markdown/CSV/JSON artifacts (timeline, checklist, tables, logs).
- `Learn`: Includes feedback revision plus safety/compliance support modules (currently a baseline implementation for demo use).

## Project Structure

```text
agents/       Core agents (perception/context/planner/action/safety/compliance/feedback)
tools/        Tool layer (document read, extraction, task generation, timeline, checklist, logging)
memory/       Feedback and example memory modules
evaluation/   Evaluation scripts and test cases
tests/        Unit tests
data/         Input data (assignment brief, rubric, few-shot examples)
outputs/      Generated output artifacts
main.py       CLI entry point
demo_dashboard.py  Streamlit demo dashboard
```

## Requirements

- Python 3.10+
- Dependencies in `requirements.txt`:
  - `openai`
  - `python-dotenv`
  - `streamlit`

Install:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file at project root:

```env
DEEPSEEK_API_KEY=your_api_key
DEEPSEEK_MODEL=deepseek-v4-flash
MAX_BRIEF_CHARS=60000
```

Notes:

- Requirement extraction (`Perceive`) and available-days inference (`Context`) use the DeepSeek API.
- `Reason-only` mode can run without LLM calls and is suitable for deterministic demos.

## Run Modes

### 1) Full pipeline (Perceive + Context + Reason + Action)

```bash
python main.py
```

### 2) Reason stage only (without Perceive/Context)

```bash
python main.py --reason_only --user_input "Please generate a coding plan for AssignmentPilot."
```

### 3) Action stage only (with built-in mock planner output)

```bash
python main.py --action_only
```

### 4) With explicit arguments

```bash
python main.py --brief data/assignment_brief.txt --group_size 5 --available_days 10 --topic "AssignmentPilot"
```

Available arguments:

- `--brief`: path to assignment brief file.
- `--user_input`: user request text (used by Perceive/Reason).
- `--action_only`: run Action stage only.
- `--reason_only`: run Reason stage only.
- `--group_size`: override inferred team size.
- `--available_days`: override inferred available days.
- `--topic`: selected project topic.

## Output Artifacts

Running the Action stage generates files under `outputs/`:

- `project_plan.md`: timeline and Mermaid Gantt chart.
- `compliance_report.md`: human verification checklist template.
- `task_breakdown.csv`: member task allocation table.
- `priorities.csv`: development priority table.
- `demo_log.json`: tool execution trace (observability evidence).

## Tests

Run Member 2 reasoning tests:

```bash
python -m unittest tests.test_member2_reasoning -v
```

## Local Demo Console

This branch also includes a Streamlit demo console for presenting the merged group project in a more visual way:

```bash
pip install -r requirements.txt
python -m streamlit run demo_dashboard.py
```

The console runs deterministic Reason and Action stages by default, so it can be shown without spending LLM calls. It is designed as a group presentation screen:

- `Flow`: explains how Perceive, Context, Reason, Action, and Learn map to the assignment stages.
- `Member 2 Plan`: highlights IntentRouter, PlannerAgent, TaskGenerator, and TeamAllocator.
- `Generated Files`: shows ActionAgent outputs from `outputs/`.
- `Logs`: shows observability evidence for the demo flow.
- `Raw Data`: keeps the structured JSON outputs available for technical questions.

For a Member 2 presentation, use this path:

1. Select a 4, 5, or 6-member scenario in the sidebar.
2. Click `Run Planning Demo`.
3. Open `Member 2 Plan` and explain the generated intent, team allocation, coding task timeline, and how this structured plan feeds ActionAgent.

## Declaration

After completing the agent architecture and workflow design, we used AI assistance to accelerate coding and implementation efficiency. All submitted work has been reviewed by us, and we have fully understood and mastered the related concepts, logic, and code.
