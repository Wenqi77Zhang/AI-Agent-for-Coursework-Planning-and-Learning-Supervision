import datetime
from typing import List, Dict, Any

class EvalReportGenerator:
    """
    生成系统评估报告 (Markdown 格式)。
    此报告可作为 Action 阶段的输出展示，体现 Agent 的可观测性和评估能力。
    """
    def __init__(self):
        pass

    def generate_markdown_report(self, results: List[Dict[str, Any]], metrics: Dict[str, float], output_path: str = "outputs/evaluation_report.md"):
        """将测试结果写入 Markdown 文件"""
        
        report_lines = [
            "# AssignmentPilot 代理评估报告 (Agent Evaluation Report)",
            f"**生成时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**整体通过率**: {metrics['pass_rate']}%\n",
            "## 测试用例明细"
        ]
        
        for res in results:
            status_icon = "✅" if res["passed"] else "❌"
            report_lines.append(f"### {status_icon} {res['id']}: {res['description']}")
            report_lines.append(f"- **测试结果**: {'通过' if res['passed'] else '失败'}")
            report_lines.append(f"- **详细信息**: {res['details']}")
            report_lines.append("")
            
        report_content = "\n".join(report_lines)
        
        # 实际运行中如果报错找不到 outputs 目录，需提前建好该文件夹
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(report_content)
            print(f"📄 评估报告已成功导出至: {output_path}")
        except Exception as e:
            print(f"❌ 导出报告失败: {e}")
            
        return report_content