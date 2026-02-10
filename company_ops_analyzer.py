#!/usr/bin/env python3
"""公司运营分析自动化工具。

功能:
1. 读取订单 CSV 数据
2. 自动计算核心经营指标
3. 输出 JSON 报告

CSV 字段要求:
- order_id
- date (YYYY-MM-DD)
- department
- revenue
- cost
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


@dataclass
class OrderRecord:
    order_id: str
    date: datetime
    department: str
    revenue: float
    cost: float

    @property
    def profit(self) -> float:
        return self.revenue - self.cost


class OpsAnalyzer:
    """公司运营分析器。"""

    def __init__(self, records: Iterable[OrderRecord]) -> None:
        self.records = list(records)

    def summary(self) -> dict:
        total_revenue = sum(r.revenue for r in self.records)
        total_cost = sum(r.cost for r in self.records)
        total_profit = total_revenue - total_cost
        order_count = len(self.records)

        profit_margin = (total_profit / total_revenue) if total_revenue else 0.0
        avg_order_revenue = (total_revenue / order_count) if order_count else 0.0

        by_department: dict[str, dict[str, float]] = defaultdict(
            lambda: {"orders": 0, "revenue": 0.0, "cost": 0.0, "profit": 0.0}
        )

        for record in self.records:
            metric = by_department[record.department]
            metric["orders"] += 1
            metric["revenue"] += record.revenue
            metric["cost"] += record.cost
            metric["profit"] += record.profit

        top_department = None
        if by_department:
            top_department = max(by_department.items(), key=lambda item: item[1]["profit"])[0]

        return {
            "overview": {
                "order_count": order_count,
                "total_revenue": round(total_revenue, 2),
                "total_cost": round(total_cost, 2),
                "total_profit": round(total_profit, 2),
                "profit_margin": round(profit_margin, 4),
                "avg_order_revenue": round(avg_order_revenue, 2),
            },
            "department_metrics": {
                dep: {
                    "orders": int(values["orders"]),
                    "revenue": round(values["revenue"], 2),
                    "cost": round(values["cost"], 2),
                    "profit": round(values["profit"], 2),
                }
                for dep, values in sorted(by_department.items())
            },
            "insights": {
                "top_department_by_profit": top_department,
            },
        }


def load_records(csv_path: Path) -> list[OrderRecord]:
    records: list[OrderRecord] = []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        required_fields = {"order_id", "date", "department", "revenue", "cost"}
        if not required_fields.issubset(set(reader.fieldnames or [])):
            missing = required_fields.difference(set(reader.fieldnames or []))
            raise ValueError(f"CSV 缺少字段: {', '.join(sorted(missing))}")

        for row in reader:
            records.append(
                OrderRecord(
                    order_id=row["order_id"],
                    date=datetime.strptime(row["date"], "%Y-%m-%d"),
                    department=row["department"],
                    revenue=float(row["revenue"]),
                    cost=float(row["cost"]),
                )
            )

    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="公司运营分析自动化工具")
    parser.add_argument("input_csv", type=Path, help="输入的订单 CSV 文件路径")
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
