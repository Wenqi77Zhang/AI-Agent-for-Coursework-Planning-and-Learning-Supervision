from typing import Dict, List, Any
from evaluation.test_cases import TEST_CASES
from agents.safety_agent import SafetyAgent
from agents.compliance_agent import ComplianceAgent

class Evaluator:
    """
    主动式评估引擎。
    批量运行测试用例，计算 Agent 准确率。
    """
    def __init__(self):
        self.safety_agent = SafetyAgent()
        self.compliance_agent = ComplianceAgent()

    def run_evaluations(self) -> List[Dict[str, Any]]:
        results = []
        
        for case in TEST_CASES:
            case_result = {
                "id": case["id"],
                "description": case["description"],
                "passed": False,
                "details": ""
            }
            
            if case["category"] == "safety":
                response = self.safety_agent.run(case["input"])
                is_safe = response["is_safe"]
                if is_safe == case["expected_is_safe"]:
                    case_result["passed"] = True
                case_result["details"] = f"Expected is_safe={case['expected_is_safe']}, Got is_safe={is_safe}. Reason: {response['reason']}"
                
            elif case["category"] == "compliance":
                response = self.compliance_agent.run(case["input_plan"])
                is_compliant = response["is_compliant"]
                if is_compliant == case["expected_is_compliant"]:
                    case_result["passed"] = True
                case_result["details"] = f"Missing items: {response['missing_items']}"
                
            results.append(case_result)
            
        return results

    def get_metrics(self, results: List[Dict[str, Any]]) -> Dict[str, float]:
        """计算通过率"""
        if not results:
            return {"pass_rate": 0.0}
        passed_count = sum(1 for r in results if r["passed"])
        return {"pass_rate": round(passed_count / len(results) * 100, 2)}