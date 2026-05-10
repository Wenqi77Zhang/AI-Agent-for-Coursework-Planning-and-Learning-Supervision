# agents/compliance_agent.py

from typing import Dict, Any, List

class ComplianceAgent:
    """
    合规检查 Agent。
    评估生成的项目计划是否满足 CA6123 的作业简报要求。
    """
    def __init__(self):
        # 根据 CA6123 Assignment Brief 提取的核心必须项
        self.required_items = [
            "Overview", "Perceive", "Reason", "Action", "Learn", 
            "AI-Human Interaction", "Responsible Agentic AI", "Conclusions",
            "12分钟视频" # 视频时长限制
        ]

    def check_plan(self, current_plan_text: str) -> Dict[str, Any]:
        """
        检查当前计划中是否遗漏了核心评分点。
        """
        missing_items = []
        for item in self.required_items:
            # 简单的文本匹配，实际可使用 LLM 语义检查以提高准确率
            if item.lower() not in current_plan_text.lower():
                missing_items.append(item)
                
        is_compliant = len(missing_items) == 0
        
        recommendations = []
        if not is_compliant:
            recommendations.append("生成的计划不符合 CA6123 作业基本要求，请补充缺失模块。")
            if "Responsible Agentic AI" in missing_items:
                recommendations.append("建议：加入 Safety Agent 来展示负责任的 AI 设计。")
            if "Learn" in missing_items:
                recommendations.append("建议：加入 Few-shot 示例或反馈记忆机制来展示 Learn 阶段。")

        return {
            "is_compliant": is_compliant,
            "missing_items": missing_items,
            "recommendations": recommendations
        }

    def run(self, current_plan: str) -> Dict[str, Any]:
        return self.check_plan(current_plan)