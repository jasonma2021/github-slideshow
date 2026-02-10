from pathlib import Path

from company_ops_analyzer import OpsAnalyzer, load_records


def test_load_records_and_summary() -> None:
    sample_path = Path("data/sample_orders.csv")
    records = load_records(sample_path)
    assert len(records) == 6

    summary = OpsAnalyzer(records).summary()
    assert summary["overview"]["doc_count"] == 6
    assert summary["overview"]["total_revenue"] == 67805.0
    assert summary["overview"]["total_cost"] == 139220.0
    assert summary["overview"]["total_profit"] == -71415.0

    chain_metrics = summary["supply_chain_metrics"]
    assert chain_metrics["purchase_inbound_qty"] == 180.0
    assert chain_metrics["sale_outbound_qty"] == 95.0
    assert chain_metrics["inventory_balance_qty"] == 78.0

    trace_t001 = summary["traceability"]["T001"]
    assert trace_t001["event_count"] == 3
    assert trace_t001["events"][0]["stage"] == "采购入库"
    assert trace_t001["events"][-1]["stage"] == "销售出库"

    assert summary["insights"]["top_department_by_profit"] == "销售"

    product_dimension = summary["dimension_coverage"]["商品资料"]
    assert all(metric["missing"] == 0 for metric in product_dimension.values())


def test_demo_profitable_chain_has_positive_sales_profit() -> None:
    records = load_records(Path("data/demo_profitable_chain.csv"))
    summary = OpsAnalyzer(records).summary()

    assert summary["overview"]["doc_count"] == 6
    assert summary["department_metrics"]["销售"]["profit"] > 0
    assert set(summary["traceability"].keys()) == {"DT1001", "DT1002"}
