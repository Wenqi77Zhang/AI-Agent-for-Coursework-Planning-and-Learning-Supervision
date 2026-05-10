from typing import List

class FeedbackMemory:
    """
    用户反馈记忆库。
    记录用户在 Human-in-the-loop 环节给出的修改建议。
    Stores user suggestions during Human-in-the-loop interactions.
    """
    def __init__(self):
        # 存储反馈字符串的列表
        self.history: List[str] = []

    def add_feedback(self, feedback: str):
        """
        添加一条新的用户反馈（支持中英双语）。
        Add a new piece of user feedback (Supports EN/ZH).
        """
        if feedback and len(feedback.strip()) > 0:
            self.history.append(feedback.strip())

    def get_history_summary(self) -> str:
        """
        获取反馈历史摘要。
        Get a summary of the feedback history for the LLM context.
        """
        if not self.history:
            return "No previous feedback. / 暂无历史反馈。"
        
        # 将多条反馈串联起来
        summary = "Feedback sequence / 反馈序列: "
        summary += " -> ".join([f"[{f}]" for f in self.history])
        return summary

    def clear(self):
        """清空记忆 / Clear memory"""
        self.history = []