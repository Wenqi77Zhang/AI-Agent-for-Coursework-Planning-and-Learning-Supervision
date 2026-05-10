import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from evaluation.evaluator import Evaluator
from evaluation.eval_report import EvalReportGenerator

print("开始运行安全与合规测试...")
my_evaluator = Evaluator()
results = my_evaluator.run_evaluations()
metrics = my_evaluator.get_metrics(results)

report_gen = EvalReportGenerator()
report_gen.generate_markdown_report(results, metrics, output_path="outputs/compliance_report.md")
print("测试完成！请查看outputs/compliance_report.md")