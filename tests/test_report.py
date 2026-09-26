import json

from relmote.report import export_support_report
from relmote.software_node import SoftwareNode


def test_support_report_exports_current_tasks(tmp_path):
    node = SoftwareNode()
    node.start_observe_session()
    node.run_task("diagnose-network")

    path = export_support_report(node, tmp_path / "report.json")
    value = json.loads(path.read_text())

    assert value["format"] == "relmote-support-report-v0"
    assert value["state"]["tasks"]
    assert "Inspect before sharing" in value["warning"]
