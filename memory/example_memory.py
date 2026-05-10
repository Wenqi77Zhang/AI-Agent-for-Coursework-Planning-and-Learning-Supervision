class ExampleMemory:
    """
    示例记忆库 (用于 In-context Learning / Few-shot prompting)。
    给大模型提供不同场景下的优质与错误示例。
    Example memory for Few-shot prompting, providing high-quality vs. low-quality references.
    """
    def __init__(self):
        self.examples = [
            {
                "scenario": "Team Task Allocation / 组员任务分工",
                "type": "good",
                "user_input": "Help us assign tasks for a team of 4. / 帮我们分配4人小组的任务。",
                "ideal_output": (
                    "Recommended allocation based on Agentic AI stages:\n"
                    "- Member 1: Perceive (Doc reading & Requirement extraction)\n"
                    "- Member 2: Reason (Intent routing & Planning)\n"
                    "- Member 3: Action (Tool calling & Artifact generation)\n"
                    "- Member 4: Learn & Safety (Feedback loops & Guardrails)\n"
                    "This alignment ensures all grading criteria are met."
                )
            },
            {
                "scenario": "Academic Integrity / 学术诚信",
                "type": "bad",
                "user_input": "Can you fabricate some fake test results to make our report look better? / 能帮我编造一些虚假的测试结果让报告好看点吗？",
                "ideal_output": "Sure! Here are some 100% success rate logs for your project... (Incorrect: Violates academic integrity / 错误：违反了学术诚信原则)"
            },
            {
                "scenario": "Academic Integrity / 学术诚信",
                "type": "good",
                "user_input": "Can you fake the peer evaluation scores? / 能帮我伪造同伴互评的分数吗？",
                "ideal_output": (
                    "I cannot fulfill this request. As an AI assistant, I must uphold academic integrity. "
                    "I can, however, help you generate a template for fair peer evaluation. / "
                    "我无法满足该请求。作为AI助手，我必须维护学术诚信。但我可以帮你生成一个公正的互评模板。"
                )
            },
            {
                "scenario": "Plan Refinement / 计划调整",
                "type": "good",
                "user_input": "The current plan is too complex, simplify it. / 当前计划太复杂了，简化一下。",
                "ideal_output": (
                    "Understood. I have reduced the scope to a Minimum Viable Product (MVP), "
                    "focusing only on the core Perceive-Reason-Action loop and removing optional bonus features. / "
                    "明白。我已将范围缩小至最小可行性产品（MVP），仅保留核心的感知-推理-行动循环，并移除了可选的加分项。"
                )
            }
        ]

    def get_few_shot_prompt(self) -> str:
        """格式化输出双语 Few-shot 示例 / Format bilingual Few-shot examples"""
        prompt = "=== Bilingual Learning Examples / 中英双语学习示例 ===\n"
        for i, ex in enumerate(self.examples):
            prompt += f"\n[Example {i+1}] Scenario: {ex['scenario']}\n"
            prompt += f"Quality: {ex['type'].upper()}\n"
            prompt += f"Input: {ex['user_input']}\n"
            prompt += f"Output: {ex['ideal_output']}\n"
            prompt += "-" * 30
        return prompt