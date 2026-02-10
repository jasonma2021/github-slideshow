# Your GitHub Learning Lab Repository for Introducing GitHub

Welcome to **your** repository for your GitHub Learning Lab course. This repository will be used during the different activities that I will be guiding you through. See a word you don't understand? We've included an emoji 📖 next to some key terms. Click on it to see its definition.

Oh! I haven't introduced myself...

I'm the GitHub Learning Lab bot and I'm here to help guide you in your journey to learn and master the various topics covered in this course. I will be using Issue and Pull Request comments to communicate with you. In fact, I already added an issue for you to check out.

![issue tab](https://lab.github.com/public/images/issue_tab.png)

I'll meet you over there, can't wait to get started!

This course is using the :sparkles: open source project [reveal.js](https://github.com/hakimel/reveal.js/). In some cases we’ve made changes to the history so it would behave during class, so head to the original project repo to learn more about the cool people behind this project.

## 公司运营分析自动化工具

仓库中提供可独立运行的脚本 `company_ops_analyzer.py`，用于自动处理进销存业务数据，按基础资料维度分析并生成“全链条追溯”报告。

### 功能
- 读取进销存 CSV 数据（采购入库 / 销售出库 / 库存调整）
- 按基础资料维度校验字段完整性（商品、价格、业务、财务、期初）
- 自动汇总核心经营指标：总营收、总成本、总利润、毛利率、平均单据营收
- 输出供应链指标：采购入库量、销售出库量、库存结余量、按业务类型统计
- 输出 trace_id 维度的全链条追溯事件清单（可追踪每条链路的单据流转）

### CSV 字段（核心）
必须包含字段：
- 核心交易：`doc_id,trace_id,date,biz_type,product_name,qty,revenue,cost`
- 基础资料维度：
  - 商品资料：`unit,brand,tag,attribute,barcode`
  - 价格设置：`product_price,customer_price,supplier_price,price_priority,purchase_limit_price,sale_limit_price,promotion_policy`
  - 业务资料：`customer,supplier,department,employee,warehouse,bin_location,income_category,expense_category,settlement_term,logistics_company`
  - 财务资料：`currency,payment_method,account,subject,voucher_word,voucher_template,electronic_archive`
  - 期初录入：`opening_inventory,opening_consignment_balance,opening_customer_balance,opening_supplier_balance,opening_finance_balance,opening_cashflow_balance,opening_account_balance`

其中 `biz_type` 仅支持：`purchase_inbound`、`sale_outbound`、`inventory_adjustment`。

### 快速开始
```bash
python3 company_ops_analyzer.py data/sample_orders.csv -o ops_report.json
```

### 运行测试
```bash
python3 -m pytest -q
```

### Demo 数据模拟与报表产出
已提供 3 份可直接运行的数据：
- `data/sample_orders.csv`
- `data/demo_profitable_chain.csv`
- `data/demo_cost_pressure_chain.csv`

运行以下命令可模拟分析并生成报表：
```bash
python3 company_ops_analyzer.py data/sample_orders.csv -o reports/sample_orders_report.json
python3 company_ops_analyzer.py data/demo_profitable_chain.csv -o reports/demo_profitable_chain_report.json
python3 company_ops_analyzer.py data/demo_cost_pressure_chain.csv -o reports/demo_cost_pressure_chain_report.json
```

生成结果示例位于 `reports/` 目录。
