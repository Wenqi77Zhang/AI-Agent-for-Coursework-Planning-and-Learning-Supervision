import csv
import json
from html import escape
from pathlib import Path
from typing import Any, Dict, Iterable, List

import streamlit as st

from agents.action_agent import ActionAgent
from main import run_reasoning_demo


PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_ROOT / "outputs"

SCENARIOS = {
    "Coding plan": "Please generate a coding plan for AssignmentPilot and allocate tasks for our team.",
    "5-member team": "We are a 5-member group. Please generate the project plan and task allocation.",
    "6-member team": "We are a 6-member group. Please plan the architecture, coding tasks, and presentation focus.",
    "Video demo": "Please help us prepare a concise video demo structure for AssignmentPilot.",
    "Revision": "This plan is too complex. Please simplify it into a realistic MVP.",
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []

    with path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def run_reason(user_input: str, group_size: int, available_days: int, topic: str) -> Dict[str, Any]:
    return run_reasoning_demo(
        user_input=user_input,
        group_size=group_size,
        available_days=available_days,
        selected_topic=topic,
        print_output=False,
    )


def run_action(plan_data: Dict[str, Any]) -> Any:
    demo_log_path = OUTPUT_DIR / "demo_log.json"
    if demo_log_path.exists():
        demo_log_path.unlink()

    action_agent = ActionAgent()
    return action_agent.run_actions(plan_data)


def combined_logs(
    intent_response: Any,
    plan_response: Any,
    action_response: Any | None,
) -> List[Dict[str, Any]]:
    logs = intent_response.logs + plan_response.logs
    if action_response is not None:
        logs += action_response.logs
    return logs


def stage_state(plan_data: Dict[str, Any], action_response: Any | None) -> Dict[str, str]:
    return {
        "Perceive": "Ready",
        "Context": "Ready",
        "Reason": "Complete" if plan_data.get("coding_tasks") else "Waiting",
        "Action": "Complete" if action_response is not None else "Ready",
        "Learn": "Pending",
    }


def inject_css() -> None:
    st.markdown(
        """
<style>
:root {
  --paper: #f5f5f7;
  --ink: #1d1d1f;
  --muted: #6e6e73;
  --line: rgba(29, 29, 31, 0.10);
  --surface: rgba(255, 255, 255, 0.94);
  --blue: #0071e3;
  --blue-soft: rgba(0, 113, 227, 0.11);
  --green-soft: rgba(52, 199, 89, 0.15);
  --orange-soft: rgba(255, 159, 10, 0.15);
  --red-soft: rgba(255, 59, 48, 0.11);
  --shadow: 0 22px 70px rgba(0, 0, 0, 0.08);
}

html, body, .stApp, [data-testid="stAppViewContainer"] {
  overflow-x: hidden;
}

.stApp {
  background:
    radial-gradient(circle at 12% 5%, rgba(0, 113, 227, 0.16), transparent 26%),
    radial-gradient(circle at 88% 12%, rgba(52, 199, 89, 0.10), transparent 24%),
    linear-gradient(180deg, #ffffff 0%, var(--paper) 48%, #ffffff 100%);
  color: var(--ink);
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", sans-serif;
}

.block-container {
  max-width: 1240px;
  padding-top: 5rem;
  padding-bottom: 4rem;
}

header[data-testid="stHeader"] {
  background: transparent;
}

section[data-testid="stSidebar"] {
  background: rgba(255, 255, 255, 0.82);
  border-right: 1px solid var(--line);
  backdrop-filter: blur(26px);
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
  color: var(--muted);
}

.hero {
  border: 1px solid var(--line);
  border-radius: 28px;
  padding: 28px;
  background: linear-gradient(135deg, rgba(255,255,255,0.96), rgba(255,255,255,0.76));
  box-shadow: var(--shadow);
  backdrop-filter: blur(24px);
  margin-bottom: 18px;
}

.hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(280px, 0.85fr);
  gap: 24px;
  align-items: stretch;
}

.brand-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.brand-mark {
  width: 42px;
  height: 42px;
  border-radius: 14px;
  display: grid;
  place-items: center;
  color: white;
  font-weight: 800;
  background: linear-gradient(145deg, #0a84ff, #30d158);
  box-shadow: 0 16px 34px rgba(0, 113, 227, 0.22);
}

.brand-title {
  font-size: 15px;
  font-weight: 780;
  color: var(--ink);
}

.brand-subtitle {
  color: var(--muted);
  font-size: 12px;
  margin-top: 2px;
}

.hero h1 {
  margin: 0;
  max-width: 760px;
  color: var(--ink);
  font-size: clamp(34px, 5vw, 54px);
  line-height: 1.04;
  letter-spacing: 0;
}

.hero-copy {
  max-width: 700px;
  color: var(--muted);
  margin: 14px 0 0;
  font-size: 16px;
  line-height: 1.55;
}

.runbook {
  background: rgba(245, 245, 247, 0.84);
  border: 1px solid var(--line);
  border-radius: 22px;
  padding: 16px;
}

.runbook-title {
  font-size: 15px;
  font-weight: 780;
  color: var(--ink);
  margin-bottom: 10px;
}

.run-step {
  display: grid;
  grid-template-columns: 34px minmax(0, 1fr);
  gap: 12px;
  padding: 11px 0;
  border-top: 1px solid var(--line);
}

.run-step:first-of-type {
  border-top: 0;
  padding-top: 0;
}

.step-number {
  width: 30px;
  height: 30px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  background: var(--blue-soft);
  color: var(--blue);
  font-weight: 800;
  font-size: 13px;
}

.step-title {
  color: var(--ink);
  font-weight: 720;
  font-size: 14px;
  margin-bottom: 3px;
}

.step-copy,
.small-copy {
  color: var(--muted);
  font-size: 12px;
  line-height: 1.45;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 12px;
  margin: 18px 0 10px;
}

.kpi {
  min-width: 0;
  padding: 16px;
  border-radius: 20px;
  background: var(--surface);
  border: 1px solid var(--line);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.045);
}

.kpi-label {
  color: var(--muted);
  font-size: 12px;
  margin-bottom: 8px;
}

.kpi-value {
  color: var(--ink);
  font-size: clamp(20px, 2.5vw, 25px);
  font-weight: 800;
  line-height: 1.1;
  overflow-wrap: anywhere;
}

div[data-testid="stTabs"] {
  margin-top: 14px;
}

div[data-testid="stTabs"] [role="tablist"] {
  gap: 8px;
  padding: 7px;
  border: 1px solid var(--line);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.70);
  overflow-x: auto;
}

div[data-testid="stTabs"] button[role="tab"] {
  min-height: 38px;
  padding: 8px 14px;
  border-radius: 13px;
  color: var(--ink) !important;
  background: transparent;
  white-space: nowrap;
}

div[data-testid="stTabs"] button[role="tab"] p {
  color: inherit !important;
  font-weight: 720;
  font-size: 13px;
}

div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
  background: white;
  color: var(--blue) !important;
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.08);
}

div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
  display: none;
}

.section-head {
  margin: 26px 0 12px;
}

.section-head h2 {
  font-size: 24px;
  line-height: 1.15;
  letter-spacing: 0;
  margin: 0;
  color: var(--ink);
}

.section-head p {
  margin: 7px 0 0;
  color: var(--muted);
  font-size: 14px;
  line-height: 1.5;
}

.stage-map {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(178px, 1fr));
  gap: 12px;
}

.stage-card,
.member-card,
.task-card,
.artifact-card,
.log-card {
  min-width: 0;
  border: 1px solid var(--line);
  background: var(--surface);
  border-radius: 22px;
  padding: 17px;
  box-shadow: 0 10px 28px rgba(0,0,0,0.045);
}

.stage-card {
  min-height: 148px;
}

.stage-index {
  font-size: 12px;
  color: var(--muted);
  margin-bottom: 16px;
}

.stage-name,
.member-name,
.task-title,
.artifact-title,
.log-title {
  color: var(--ink);
  font-weight: 790;
  font-size: 16px;
  line-height: 1.35;
  overflow-wrap: anywhere;
}

.stage-name {
  font-size: 18px;
  margin-bottom: 10px;
}

.stage-owner,
.member-role,
.task-meta,
.artifact-copy,
.log-copy {
  color: var(--muted);
  font-size: 13px;
  line-height: 1.5;
  overflow-wrap: anywhere;
}

.badge {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 5px 10px;
  font-size: 12px;
  font-weight: 720;
  margin-bottom: 9px;
}

.badge-complete { background: var(--green-soft); color: #0f6b2f; }
.badge-ready { background: var(--orange-soft); color: #7a4c00; }
.badge-pending { background: var(--red-soft); color: #7d1d16; }
.badge-waiting { background: var(--blue-soft); color: #0054ad; }

.member-grid,
.artifact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 14px;
}

.member-header,
.artifact-header,
.log-header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: flex-start;
  margin-bottom: 12px;
}

.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin-top: 12px;
}

.chip {
  padding: 5px 9px;
  border-radius: 999px;
  background: var(--blue-soft);
  color: #0054ad;
  font-size: 12px;
  font-weight: 680;
}

.timeline {
  display: grid;
  gap: 11px;
}

.task-card {
  display: grid;
  grid-template-columns: 54px minmax(0, 1fr) auto;
  gap: 14px;
  align-items: center;
}

.task-id {
  width: 46px;
  height: 46px;
  border-radius: 15px;
  display: grid;
  place-items: center;
  color: white;
  font-weight: 800;
  background: linear-gradient(145deg, #0071e3, #64d2ff);
}

.priority {
  justify-self: end;
  border-radius: 999px;
  padding: 7px 10px;
  font-size: 12px;
  font-weight: 760;
  background: rgba(29, 29, 31, 0.06);
  color: var(--ink);
}

.file-path {
  margin-top: 10px;
  padding: 10px;
  border-radius: 14px;
  background: #f5f5f7;
  color: var(--muted);
  font-size: 12px;
  word-break: break-all;
  font-family: "SF Mono", Consolas, monospace;
}

.empty-state {
  padding: 22px;
  border-radius: 22px;
  border: 1px dashed rgba(29, 29, 31, 0.18);
  color: var(--muted);
  background: rgba(255,255,255,0.64);
}

.stButton > button {
  border-radius: 999px;
  border: 0;
  min-height: 46px;
  background: #0071e3;
  color: white;
  font-weight: 780;
  box-shadow: 0 14px 28px rgba(0, 113, 227, 0.24);
}

.stButton > button:hover {
  background: #0066cc;
  color: white;
}

div[data-testid="stDataFrame"] {
  border-radius: 18px;
  overflow: hidden;
  border: 1px solid var(--line);
}

@media (max-width: 800px) {
  .block-container { padding-top: 4rem; }
  .hero { padding: 22px; }
  .hero-grid { grid-template-columns: 1fr; }
  .task-card { grid-template-columns: 1fr; }
  .priority { justify-self: start; }
}
</style>
        """,
        unsafe_allow_html=True,
    )


def section_head(title: str, copy: str) -> None:
    st.markdown(
        (
            '<div class="section-head">'
            f'<h2>{escape(title)}</h2>'
            f'<p>{escape(copy)}</p>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown(
        (
            '<div class="hero">'
            '<div class="brand-row">'
            '<div class="brand-mark">AP</div>'
            '<div>'
            '<div class="brand-title">AssignmentPilot Demo Console</div>'
            '<div class="brand-subtitle">Reasoning, planning, tool execution, and evidence in one local view</div>'
            '</div>'
            '</div>'
            '<div class="hero-grid">'
            '<div>'
            '<h1>Present the agent workflow, not just terminal output.</h1>'
            '<p class="hero-copy">Choose a team size, run the plan, show Member 2 reasoning, then open Action artifacts and logs as evidence.</p>'
            '</div>'
            '<div class="runbook">'
            '<div class="runbook-title">Demo steps</div>'
            '<div class="run-step"><div class="step-number">1</div><div><div class="step-title">Choose a scenario</div><div class="step-copy">Use the sidebar presets for coding plan, 5-member, 6-member, video demo, or revision.</div></div></div>'
            '<div class="run-step"><div class="step-number">2</div><div><div class="step-title">Run the pipeline</div><div class="step-copy">Click Run Planning Demo to execute IntentRouter, PlannerAgent, and ActionAgent.</div></div></div>'
            '<div class="run-step"><div class="step-number">3</div><div><div class="step-title">Show the evidence</div><div class="step-copy">Use Flow, Member 2 Plan, Generated Files, and Logs from left to right.</div></div></div>'
            '</div>'
            '</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def render_kpis(plan_data: Dict[str, Any], intent: str, group_size: int, available_days: int, action_response: Any | None) -> None:
    generated_files = action_response.data.get("generated_files", {}) if action_response else {}
    items = [
        ("Detected intent", intent),
        ("Team size", str(group_size)),
        ("Coding tasks", str(len(plan_data.get("coding_tasks", [])))),
        ("Generated files", str(len(generated_files))),
    ]
    html = ['<div class="kpi-grid">']
    for label, value in items:
        html.append(
            f'<div class="kpi"><div class="kpi-label">{escape(label)}</div><div class="kpi-value">{escape(value)}</div></div>'
        )
    html.append("</div>")
    html.append(
        f'<div class="small-copy">Available days: {available_days}. This console uses deterministic Reason and Action flows, so it is safe for a live classroom demo without LLM spending.</div>'
    )
    st.markdown("".join(html), unsafe_allow_html=True)


def render_stage_map(plan_data: Dict[str, Any], action_response: Any | None) -> None:
    stages = stage_state(plan_data, action_response)
    owners = {
        "Perceive": "Member 1 reads the brief and extracts requirements.",
        "Context": "Context resolution can infer team size and time limits.",
        "Reason": "Member 2 routes intent and builds the project plan.",
        "Action": "Member 3 generates files, checklists, and logs.",
        "Learn": "Member 4 will add feedback, safety, compliance, and evaluation.",
    }
    html = ['<div class="stage-map">']
    for index, (stage, status) in enumerate(stages.items(), start=1):
        status_class = status.lower()
        html.append(
            f'<div class="stage-card">'
            f'<div class="stage-index">Stage {index}</div>'
            f'<div class="stage-name">{escape(stage)}</div>'
            f'<span class="badge badge-{status_class}">{escape(status)}</span>'
            f'<div class="stage-owner">{escape(owners[stage])}</div>'
            f'</div>'
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def render_member_cards(team_allocation: Dict[str, Any]) -> None:
    if not team_allocation:
        st.markdown('<div class="empty-state">No team allocation generated yet.</div>', unsafe_allow_html=True)
        return

    html = ['<div class="member-grid">']
    for member, value in team_allocation.items():
        if isinstance(value, dict):
            role = value.get("role", "")
            stage = value.get("agentic_stage", "")
            modules = value.get("modules", [])
            video_focus = value.get("video_focus", "")
        else:
            role = "Contributor"
            stage = ""
            modules = value if isinstance(value, list) else [str(value)]
            video_focus = ""

        chips = "".join(f'<span class="chip">{escape(str(module))}</span>' for module in modules)
        html.append(
            f'<div class="member-card">'
            f'<div class="member-header">'
            f'<div>'
            f'<div class="member-name">{escape(member)}</div>'
            f'<div class="member-role">{escape(role)}</div>'
            f'</div>'
            f'<span class="badge badge-ready">{escape(stage)}</span>'
            f'</div>'
            f'<div class="member-role">{escape(video_focus)}</div>'
            f'<div class="chip-row">{chips}</div>'
            f'</div>'
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def render_task_timeline(tasks: List[Dict[str, str]]) -> None:
    if not tasks:
        st.markdown('<div class="empty-state">No coding tasks generated yet.</div>', unsafe_allow_html=True)
        return

    html = ['<div class="timeline">']
    for task in tasks:
        task_id = task.get("id", "T")
        stage = task.get("stage", "")
        owner = task.get("owner", "")
        priority = task.get("priority", "")
        title = task.get("task", "")
        output = task.get("output", "")
        html.append(
            f'<div class="task-card">'
            f'<div class="task-id">{escape(task_id)}</div>'
            f'<div>'
            f'<div class="task-title">{escape(title)}</div>'
            f'<div class="task-meta">{escape(stage)} / {escape(owner)} / Output: {escape(output)}</div>'
            f'</div>'
            f'<div class="priority">{escape(priority)}</div>'
            f'</div>'
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def render_artifacts(action_response: Any | None) -> None:
    generated_files = action_response.data.get("generated_files", {}) if action_response else {}
    labels = {
        "project_plan": ("Project plan", "Markdown timeline with a Mermaid Gantt chart."),
        "compliance_checklist": ("Compliance checklist", "Pre-submission checklist prepared for Member 4 integration."),
        "task_breakdown": ("Task breakdown", "CSV table of member responsibilities."),
        "development_priorities": ("Priorities", "CSV table of development priorities and rationale."),
        "demo_execution_logs": ("Demo logs", "JSON trace for agent observability evidence."),
    }

    if not generated_files:
        st.markdown('<div class="empty-state">Turn on Generate Action artifacts, then run the demo.</div>', unsafe_allow_html=True)
        return

    html = ['<div class="artifact-grid">']
    for key, path in generated_files.items():
        title, copy = labels.get(key, (key, "Generated output file."))
        html.append(
            f'<div class="artifact-card">'
            f'<div class="artifact-header">'
            f'<div class="artifact-title">{escape(title)}</div>'
            f'<span class="badge badge-complete">Created</span>'
            f'</div>'
            f'<div class="artifact-copy">{escape(copy)}</div>'
            f'<div class="file-path">{escape(str(path))}</div>'
            f'</div>'
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def render_log_cards(logs: Iterable[Dict[str, Any]]) -> None:
    items = list(logs)
    if not items:
        st.markdown('<div class="empty-state">No logs generated yet.</div>', unsafe_allow_html=True)
        return

    html = ['<div class="timeline">']
    for index, log in enumerate(items, start=1):
        agent = log.get("agent") or log.get("agent_context", "")
        action = log.get("action") or log.get("tool_action", "")
        status = log.get("status") or log.get("execution_status", "")
        summary = log.get("output_summary") or log.get("observation") or log.get("io_traces") or ""
        html.append(
            f'<div class="log-card">'
            f'<div class="log-header">'
            f'<div>'
            f'<div class="log-title">{index}. {escape(str(agent))} / {escape(str(action))}</div>'
            f'<div class="log-copy">{escape(str(summary))}</div>'
            f'</div>'
            f'<span class="badge badge-complete">{escape(str(status))}</span>'
            f'</div>'
            f'</div>'
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def render_markdown_preview(title: str, path: Path, max_chars: int = 3600) -> None:
    text = read_text(path)
    with st.expander(title, expanded=False):
        if text:
            st.markdown(text[:max_chars])
            if len(text) > max_chars:
                st.caption("Preview truncated for readability. Open the file for the full artifact.")
        else:
            st.caption(f"{path.name} has not been generated yet.")


def main() -> None:
    st.set_page_config(
        page_title="AssignmentPilot Demo Console",
        page_icon="AP",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()

    st.sidebar.markdown("## Demo controls")
    st.sidebar.caption("Start here during the presentation.")

    scenario = st.sidebar.radio("Scenario", list(SCENARIOS.keys()), index=0)
    default_group_size = 5 if scenario == "5-member team" else 6 if scenario == "6-member team" else 4
    user_input = st.sidebar.text_area("User request", value=SCENARIOS[scenario], height=128)
    topic = st.sidebar.text_input("Project topic", value="AssignmentPilot")
    group_size = st.sidebar.slider("Group size", min_value=4, max_value=6, value=default_group_size)
    available_days = st.sidebar.slider("Available days", min_value=1, max_value=14, value=7)
    generate_action = st.sidebar.toggle("Generate Action artifacts", value=True)
    run_clicked = st.sidebar.button("Run Planning Demo", width="stretch")

    if run_clicked or "reasoning_results" not in st.session_state:
        reasoning_results = run_reason(user_input, group_size, available_days, topic)
        st.session_state["reasoning_results"] = reasoning_results
        st.session_state["last_inputs"] = {
            "group_size": group_size,
            "available_days": available_days,
            "topic": topic,
            "scenario": scenario,
        }
        st.session_state["action_response"] = (
            run_action(reasoning_results["plan_response"].data)
            if generate_action
            else None
        )

    reasoning_results = st.session_state["reasoning_results"]
    intent_response = reasoning_results["intent_response"]
    plan_response = reasoning_results["plan_response"]
    plan_data = plan_response.data
    action_response = st.session_state.get("action_response")
    last_inputs = st.session_state.get("last_inputs", {})
    resolved_group_size = int(last_inputs.get("group_size", group_size))
    resolved_available_days = int(last_inputs.get("available_days", available_days))
    intent = intent_response.data.get("intent", "unknown")

    render_hero()
    render_kpis(plan_data, intent, resolved_group_size, resolved_available_days, action_response)

    flow_tab, member2_tab, files_tab, logs_tab, raw_tab = st.tabs([
        "Flow",
        "Member 2 Plan",
        "Generated Files",
        "Logs",
        "Raw Data",
    ])

    with flow_tab:
        section_head("Agentic workflow map", "Each stage maps to a project owner and a required CA6123 agentic capability.")
        render_stage_map(plan_data, action_response)

    with member2_tab:
        section_head("Team allocation", "PlannerAgent turns the selected team size into readable member responsibilities.")
        render_member_cards(plan_data.get("team_allocation", {}))
        section_head("Coding task timeline", "TaskGenerator keeps id, stage, owner, priority, and expected output visible.")
        render_task_timeline(plan_data.get("coding_tasks", []))

    with files_tab:
        section_head("Action artifacts", "The Reason-stage plan is passed into ActionAgent and becomes real Markdown, CSV, and JSON deliverables.")
        render_artifacts(action_response)
        section_head("Readable previews", "Open these only if the teacher asks to inspect the generated files.")
        render_markdown_preview("Project plan preview", OUTPUT_DIR / "project_plan.md")
        render_markdown_preview("Compliance checklist preview", OUTPUT_DIR / "compliance_report.md")

        task_rows = read_csv(OUTPUT_DIR / "task_breakdown.csv")
        priority_rows = read_csv(OUTPUT_DIR / "priorities.csv")
        with st.expander("CSV previews", expanded=False):
            if task_rows:
                st.markdown("#### Task breakdown")
                st.dataframe(task_rows, width="stretch", hide_index=True)
            if priority_rows:
                st.markdown("#### Development priorities")
                st.dataframe(priority_rows, width="stretch", hide_index=True)
            if not task_rows and not priority_rows:
                st.caption("CSV files have not been generated yet.")

    with logs_tab:
        section_head("Observability logs", "These cards show the execution trace that supports the Agent Observability bonus feature.")
        render_log_cards(combined_logs(intent_response, plan_response, action_response))

    with raw_tab:
        section_head("Raw structured output", "Use this tab only for technical questions. The earlier tabs are better for presentation.")
        st.markdown("#### IntentRouter response")
        st.json(intent_response.data)
        st.markdown("#### PlannerAgent response")
        st.json(plan_data)
        st.markdown("#### ActionAgent response")
        if action_response is not None:
            st.json(action_response.data)
        else:
            st.caption("ActionAgent was not run.")
        demo_log_path = OUTPUT_DIR / "demo_log.json"
        if demo_log_path.exists():
            st.markdown("#### demo_log.json")
            st.json(json.loads(read_text(demo_log_path)))


if __name__ == "__main__":
    main()