# Your GitHub Learning Lab Repository for Introducing GitHub

Welcome to **your** repository for your GitHub Learning Lab course. This repository will be used during the different activities that I will be guiding you through. See a word you don't understand? We've included an emoji 📖 next to some key terms. Click on it to see its definition.

Oh! I haven't introduced myself...

I'm the GitHub Learning Lab bot and I'm here to help guide you in your journey to learn and master the various topics covered in this course. I will be using Issue and Pull Request comments to communicate with you. In fact, I already added an issue for you to check out.

![issue tab](https://lab.github.com/public/images/issue_tab.png)

I'll meet you over there, can't wait to get started!

This course is using the :sparkles: open source project [reveal.js](https://github.com/hakimel/reveal.js/). In some cases we’ve made changes to the history so it would behave during class, so head to the original project repo to learn more about the cool people behind this project.

## 公司运营分析自动化工具

仓库中新增了一个可独立运行的脚本 `company_ops_analyzer.py`，用于自动处理公司运营订单数据并生成指标报告。

### 功能
- 读取订单 CSV 数据（字段：`order_id,date,department,revenue,cost`）
- 自动汇总核心指标：总营收、总成本、总利润、利润率、平均客单价
- 输出按部门拆分的经营指标
- 输出利润最高部门洞察

### 快速开始
```bash
python3 company_ops_analyzer.py data/sample_orders.csv -o ops_report.json
```

### 运行测试
```bash
python3 -m pytest -q
```
