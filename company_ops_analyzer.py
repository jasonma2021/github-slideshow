#!/usr/bin/env python3
"""公司运营分析自动化工具（含进销存全链条追溯）。

功能:
1. 读取进销存业务 CSV 数据
2. 基于基础资料维度进行数据完整性校验与经营分析
3. 输出包含全链条追溯信息的 JSON 报告
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

MASTER_DIMENSIONS: dict[str, list[str]] = {
    "商品资料": ["product_name", "unit", "brand", "tag", "attribute", "barcode"],
    "价格设置": [
        "product_price",
        "customer_price",
        "supplier_price",
        "price_priority",
        "purchase_limit_price",
        "sale_limit_price",
        "promotion_policy",
    ],
    "业务资料": [
        "customer",
        "supplier",
        "department",
        "employee",
        "warehouse",
        "bin_location",
        "income_category",
        "expense_category",
        "settlement_term",
        "logistics_company",
    ],
    "财务资料": [
        "currency",
        "payment_method",
        "account",
        "subject",
        "voucher_word",
        "voucher_template",
        "electronic_archive",
    ],
    "期初录入": [
        "opening_inventory",
        "opening_consignment_balance",
        "opening_customer_balance",
        "opening_supplier_balance",
        "opening_finance_balance",
        "opening_cashflow_balance",
        "opening_account_balance",
    ],
}

CORE_FIELDS = {
    "doc_id",
    "trace_id",
    "date",
    "biz_type",
    "product_name",
    "qty",
    "revenue",
    "cost",
}

ALL_REQUIRED_FIELDS = CORE_FIELDS.union(
    {field for fields in MASTER_DIMENSIONS.values() for field in fields}
)

BIZ_TYPE_LABELS = {
    "purchase_inbound": "采购入库",
    "sale_outbound": "销售出库",
    "inventory_adjustment": "库存调整",
}


@dataclass
class OpsRecord:
    doc_id: str
    trace_id: str
    date: datetime
    biz_type: str
    product_name: str
    department: str
    qty: float
    revenue: float
    cost: float
    dimensions: dict[str, str]

    @property
    def profit(self) -> float:
        return self.revenue - self.cost

    @property
    def inventory_delta(self) -> float:
        if self.biz_type == "purchase_inbound":
            return self.qty
        if self.biz_type == "sale_outbound":
            return -self.qty
        return self.qty


class OpsAnalyzer:
    """公司运营分析器。"""

    def __init__(self, records: Iterable[OpsRecord]) -> None:
        self.records = sorted(list(records), key=lambda x: (x.trace_id, x.date, x.doc_id))

    def summary(self) -> dict:
        total_revenue = sum(r.revenue for r in self.records)
        total_cost = sum(r.cost for r in self.records)
        total_profit = total_revenue - total_cost
        doc_count = len(self.records)

        gross_margin = (total_profit / total_revenue) if total_revenue else 0.0
        avg_doc_revenue = (total_revenue / doc_count) if doc_count else 0.0

        by_department: dict[str, dict[str, float]] = defaultdict(
            lambda: {"docs": 0, "revenue": 0.0, "cost": 0.0, "profit": 0.0}
        )
        biz_type_metrics: dict[str, dict[str, float]] = defaultdict(
            lambda: {"docs": 0, "qty": 0.0, "revenue": 0.0, "cost": 0.0}
        )
        trace_nodes: dict[str, list[dict[str, object]]] = defaultdict(list)

        for record in self.records:
            dep_metric = by_department[record.department]
            dep_metric["docs"] += 1
            dep_metric["revenue"] += record.revenue
            dep_metric["cost"] += record.cost
            dep_metric["profit"] += record.profit

            biz_metric = biz_type_metrics[record.biz_type]
            biz_metric["docs"] += 1
            biz_metric["qty"] += record.qty
            biz_metric["revenue"] += record.revenue
            biz_metric["cost"] += record.cost

            trace_nodes[record.trace_id].append(
                {
                    "doc_id": record.doc_id,
                    "date": record.date.strftime("%Y-%m-%d"),
                    "biz_type": record.biz_type,
                    "stage": BIZ_TYPE_LABELS.get(record.biz_type, record.biz_type),
                    "product_name": record.product_name,
                    "qty": round(record.qty, 2),
                    "inventory_delta": round(record.inventory_delta, 2),
                    "revenue": round(record.revenue, 2),
                    "cost": round(record.cost, 2),
                    "profit": round(record.profit, 2),
                }
            )

        inventory_balance = sum(r.inventory_delta for r in self.records)
        purchase_qty = sum(r.qty for r in self.records if r.biz_type == "purchase_inbound")
        sale_qty = sum(r.qty for r in self.records if r.biz_type == "sale_outbound")

        top_department = None
        if by_department:
            top_department = max(by_department.items(), key=lambda item: item[1]["profit"])[0]

        dimension_coverage = self._build_dimension_coverage()

        return {
            "overview": {
                "doc_count": doc_count,
                "total_revenue": round(total_revenue, 2),
                "total_cost": round(total_cost, 2),
                "total_profit": round(total_profit, 2),
                "gross_margin": round(gross_margin, 4),
                "avg_doc_revenue": round(avg_doc_revenue, 2),
            },
            "supply_chain_metrics": {
                "purchase_inbound_qty": round(purchase_qty, 2),
                "sale_outbound_qty": round(sale_qty, 2),
                "inventory_balance_qty": round(inventory_balance, 2),
                "biz_type_metrics": {
                    biz_type: {
                        "docs": int(values["docs"]),
                        "qty": round(values["qty"], 2),
                        "revenue": round(values["revenue"], 2),
                        "cost": round(values["cost"], 2),
                    }
                    for biz_type, values in sorted(biz_type_metrics.items())
                },
            },
            "department_metrics": {
                dep: {
                    "docs": int(values["docs"]),
                    "revenue": round(values["revenue"], 2),
                    "cost": round(values["cost"], 2),
                    "profit": round(values["profit"], 2),
                }
                for dep, values in sorted(by_department.items())
            },
            "dimension_coverage": dimension_coverage,
            "traceability": {
                trace_id: {
                    "event_count": len(events),
                    "events": sorted(events, key=lambda x: (x["date"], x["doc_id"])),
                }
                for trace_id, events in sorted(trace_nodes.items())
            },
            "insights": {
                "top_department_by_profit": top_department,
            },
        }

    def _build_dimension_coverage(self) -> dict[str, dict[str, dict[str, int]]]:
        result: dict[str, dict[str, dict[str, int]]] = {}
        for category, fields in MASTER_DIMENSIONS.items():
            category_metrics: dict[str, dict[str, int]] = {}
            for field in fields:
                missing_count = sum(
                    1 for record in self.records if not str(record.dimensions.get(field, "")).strip()
                )
                category_metrics[field] = {
                    "filled": len(self.records) - missing_count,
                    "missing": missing_count,
                }
            result[category] = category_metrics
        return result


def load_records(csv_path: Path) -> list[OpsRecord]:
    records: list[OpsRecord] = []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        existing_fields = set(reader.fieldnames or [])
        if not ALL_REQUIRED_FIELDS.issubset(existing_fields):
            missing = ALL_REQUIRED_FIELDS.difference(existing_fields)
            raise ValueError(f"CSV 缺少字段: {', '.join(sorted(missing))}")

        for row in reader:
            biz_type = row["biz_type"].strip()
            if biz_type not in BIZ_TYPE_LABELS:
                raise ValueError(
                    f"biz_type 仅支持 {', '.join(BIZ_TYPE_LABELS)}，收到: {biz_type}"
                )

            dimensions = {
                field: row.get(field, "").strip()
                for fields in MASTER_DIMENSIONS.values()
                for field in fields
            }
            records.append(
                OpsRecord(
                    doc_id=row["doc_id"].strip(),
                    trace_id=row["trace_id"].strip(),
                    date=datetime.strptime(row["date"].strip(), "%Y-%m-%d"),
                    biz_type=biz_type,
                    product_name=row["product_name"].strip(),
                    department=row["department"].strip(),
                    qty=float(row["qty"]),
                    revenue=float(row["revenue"]),
                    cost=float(row["cost"]),
                    dimensions=dimensions,
                )
            )

    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="公司运营分析自动化工具（支持进销存全链条追溯）")
    parser.add_argument("input_csv", type=Path, help="输入的进销存 CSV 文件路径")
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("ops_report.json"),
        help="输出的 JSON 报告路径，默认 ops_report.json",
    )
    args = parser.parse_args()

    records = load_records(args.input_csv)
    analyzer = OpsAnalyzer(records)
    report = analyzer.summary()

    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"分析完成，报告已输出到: {args.output}")


if __name__ == "__main__":
    main()
