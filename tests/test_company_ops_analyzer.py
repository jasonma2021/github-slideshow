from pathlib import Path

from company_ops_analyzer import OpsAnalyzer, load_records


def test_load_records_and_summary() -> None:
    sample_path = Path("data/sample_orders.csv")
    records = load_records(sample_path)
    assert len(records) == 6

    summary = OpsAnalyzer(records).summary()
    assert summary["overview"]["order_count"] == 6
    assert summary["overview"]["total_revenue"] == 64600.0
    assert summary["overview"]["total_cost"] == 37900.0
    assert summary["overview"]["total_profit"] == 26700.0
    assert summary["insights"]["top_department_by_profit"] == "销售"
