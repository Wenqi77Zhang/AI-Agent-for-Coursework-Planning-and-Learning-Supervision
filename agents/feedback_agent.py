from memory.feedback_memory import FeedbackMemory
from memory.example_memory import ExampleMemory

class FeedbackAgent:
    """
    反馈学习 Agent。
    结合当前计划、用户的修改意见（Feedback）以及历史记忆，生成优化后的计划。
    """
    def __init__(self):
        self.feedback_memory = FeedbackMemory()
        self.example_memory = ExampleMemory()

    def revise_plan(self, current_plan: str, user_feedback: str) -> str:
        """
        根据反馈修改计划。
        """
        # 1. 记录反馈
        self.feedback_memory.add_feedback(user_feedback)
        
        # 2. 获取上下文学习资料 (Learn 阶段)
        few_shot_context = self.example_memory.get_few_shot_prompt()
        history_context = self.feedback_memory.get_history_summary()
        
        # 3. 组装发给大模型的 Prompt
        prompt = f"""
        你是一个项目计划优化专家。
        
        {few_shot_context}
        
        当前的历史用户偏好: {history_context}
        
        ---
        目前的计划:
        {current_plan}
        
        用户的最新修改意见:
        {user_feedback}
        
        请根据用户的意见，修改并输出一份新的计划。
        """
        
        # ！！！这里需要调用你们的 LLM API ！！！
        # 比如: new_plan = llm_client.generate(prompt)
        # 为了演示，此处返回模拟文本
        
        print("💡 [Feedback Agent] 正在根据反馈进行思考和自我调整 (Learn Stage)...")
        simulated_new_plan = current_plan + f"\n\n[修订说明]: 已根据用户意见 '{user_feedback}' 调整了计划范围。"
        
        return simulated_new_plan

    def run(self, current_plan: str, user_feedback: str) -> str:
        return self.revise_plan(current_plan, user_feedback)