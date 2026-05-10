# agents/safety_agent.py

import re
from typing import Dict, Any

class SafetyAgent:
    """
    负责系统安全的 Agent (双语增强版/Bilingual Version)。
    拦截学术不端、违规代写、隐藏 AI 使用等不当请求。
    Intercepts academic misconduct, unauthorized code generation, and attempts to hide AI usage.
    """
    def __init__(self):
        # 1. 基础规则护栏：中英文危险关键词黑名单 (Bilingual Blocked Keywords)
        self.blocked_keywords = [
            "编造", "代写全部代码", "绕过", "隐藏", "隐藏AI", 
            "伪造贡献", "作弊", "保证满分",
            "fabricate", "fake", "write all code", "bypass", 
            "hide", "hide ai", "cheat", "guarantee full marks"
        ]
        
    def analyze_request(self, user_input: str) -> Dict[str, Any]:
        """
        分析用户请求是否安全。
        返回格式: {"is_safe": bool, "reason": str, "suggestion": str}
        """
        # 将输入统一转为小写，实现英文的大小写不敏感匹配
        user_input_lower = user_input.lower() 
        
        # 1. 规则引擎检查 (第一道防线)
        for keyword in self.blocked_keywords:
            if keyword.lower() in user_input_lower:
                return {
                    "is_safe": False,
                    "reason": f"触发安全护栏：请求中包含违规意图（匹配到关键词 '{keyword}'）。 / Safety Guardrail Triggered: Illicit intent detected.",
                    "suggestion": "请遵守学术诚信原则。作为一个学习辅助 Agent，我只能协助你规划、拆解和检查任务，不能替你编造数据。 / Please adhere to academic integrity."
                }
        
        # 2. 模拟 LLM 意图检查 (第二道防线：防御 Prompt 注入等复杂绕过手段)
        # 增加中英文的 "设定" 和 "限制" 等注入词汇的拦截
        injection_keywords = [
            "忽略之前的指令", "忽略之前的设定", "不受限制", "you are now",
            "ignore previous instructions", "ignore previous settings", 
            "unrestricted", "forget previous prompts"
        ]
        
        if any(keyword.lower() in user_input_lower for keyword in injection_keywords):
            return {
                "is_safe": False,
                "reason": "触发安全护栏：检测到潜在的 Prompt Injection (提示词注入) 攻击，企图篡改系统设定。 / Safety Guardrail Triggered: Potential Prompt Injection detected.",
                "suggestion": "请提供正当的作业规划需求，不要尝试绕过安全限制。 / Please provide legitimate requests."
            }
            
        return {
            "is_safe": True,
            "reason": "请求通过安全检查。 / Request passed safety checks.",
            "suggestion": ""
        }

    def run(self, user_input: str) -> Dict[str, Any]:
        """统一的 Agent 执行接口"""
        return self.analyze_request(user_input)