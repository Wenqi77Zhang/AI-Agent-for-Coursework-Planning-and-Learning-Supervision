import os
from datetime import date, timedelta
from typing import Dict, List


class TimelineGenerator:
    """
    Tool suite for generating visual project timelines and schedules.
    """

    def generate_markdown_timeline_with_gantt(
        self,
        plan_data: List[Dict[str, str]],
        output_path: str = "outputs/project_plan.md",
    ) -> str:
        """
        Generate a Markdown timeline and Mermaid Gantt chart from planner tasks.

        Supports both Member 3 mock tasks with day/task fields and Member 2
        PlannerAgent tasks with id/stage/task/owner/priority/output fields.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        start_date = date(2026, 5, 5)

        md_content = "# CA6123 AssignmentPilot Project Timeline\n\n"
        md_content += "## Visual Progress (Mermaid Gantt)\n"
        md_content += "```mermaid\ngantt\n    title Project Development Timeline\n    dateFormat  YYYY-MM-DD\n"

        current_section = None
        for index, task in enumerate(plan_data):
            phase = task.get("stage") or task.get("day") or task.get("id") or f"Phase {index + 1}"
            task_desc = self._clean_mermaid_label(task.get("task", "Unnamed Task"))
            task_date = start_date + timedelta(days=index)

            if phase != current_section:
                md_content += f"    section {self._clean_mermaid_label(phase)}\n"
                current_section = phase

            md_content += f"    {task_desc} :a{index}, {task_date.isoformat()}, 1d\n"

        md_content += "```\n\n"

        md_content += "## Detailed Schedule\n"
        md_content += "| Phase | Owner | Priority | Core Task Description | Output |\n"
        md_content += "|---|---|---|---|---|\n"
        for index, task in enumerate(plan_data):
            phase = task.get("stage") or task.get("day") or task.get("id") or f"Phase {index + 1}"
            owner = task.get("owner", "")
            priority = task.get("priority", "")
            task_desc = task.get("task", "")
            output = task.get("output", "")
            md_content += f"| **{phase}** | {owner} | {priority} | {task_desc} | {output} |\n"

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(md_content)

        return output_path

    def _clean_mermaid_label(self, value: str) -> str:
        return str(value).replace(":", " -").replace("|", "-").replace("\n", " ").strip()