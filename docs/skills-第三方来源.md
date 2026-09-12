# 第三方投研 Skills 来源记录

> 安装日期：2026-09-09
>
> 安装位置：项目级 `.claude/skills/`（SKILL.md 格式，随本仓库 git 跟踪，仅在本仓库目录的会话生效）。与 ai-berkshire 自带 command（装在全局 `~/.claude/commands`，见 [skills-清单.md](skills-清单.md)）互不干扰。

## 为什么装这些

ai-berkshire 19 个 command 方法论强但**数据层弱**。补充两类社区 skill：

1. **A股实时数据与系统化筛选**（finskills China-market）——补足 A股无实时取数、无量化筛选的短板。
2. **美股机构动向/财报日历**（tradermonty 精选）——补足美股 13F 机构持仓与财报日历监控。

## 上游仓库

| 上游 | 许可证 | 分支/commit | 说明 |
|------|--------|-------------|------|
| [Geeksfino/finskills](https://github.com/Geeksfino/finskills) | Apache-2.0 | main @ `8722415` | 30 个投研 skill（美股 15 + A股 15），本仓库只装 China-market 15 个 |
| [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) | MIT | main @ `87010e4027` | 大型交易/量化 skill 套件，本仓库只精选其中 5 个 |

> 注：mphinance/alpha-skills 与 tradermonty 高度同源，为避免重复只装 tradermonty 一个。

## 已安装清单

### A. finskills — China-market（15 个，体系自洽，内部引用 findata-toolkit-cn 取数）

esg-screener、event-driven-detector、financial-statement-analyzer、findata-toolkit-cn、high-dividend-strategy、insider-trading-analyzer、portfolio-health-check、quant-factor-screener、risk-adjusted-return-optimizer、sector-rotation-detector、sentiment-reality-gap、small-cap-growth-identifier、suitability-report-generator、tech-hype-vs-fundamentals、undervalued-stock-screener

### B. tradermonty — 精选 5 个（与 finskills CN 无重名、理念兼容）

- **institutional-flow-tracker**：13F 机构持仓分析（SEC 免费数据）
- **earnings-calendar**：美股财报日历（FMP，可配 key，无 key 降级）
- **us-stock-analysis**：单只美股基本面+技术综合
- **value-dividend-screener**：价值/股息两段筛选（FinViz + FMP）
- **finviz-screener**：FinViz 筛选 URL 构造

## 刻意排除的项

| 排除对象 | 原因 |
|---------|------|
| finskills US-market 全部（15） | 与 China-market 同名冲突（如 scenario-analyzer、undervalued-stock-screener 两边都有），且美股侧已有 tradermonty 覆盖 |
| tradermonty 的 `scenario-analyzer` | 与 finskills CN 同名，会互相覆盖 |
| tradermonty 的 `market-news-analyst` | 与 ai-berkshire 的 `/news-pulse` 职责重叠 |
| tradermonty 其余约 70 个 | 动量/期权/加密/日内交易类，与买入持有价值理念相悖；未用 `skills-index`/`agentsets` 功能 |
| alpha-skills（mphinance）全量 | 与 tradermonty 同源 |

## 使用注意

- **A股取数**：findata-toolkit-cn 走 AKShare，免费无 API key，需 Python。用前按各 skill `requirements.txt` 装依赖：`pip install -r .claude/skills/<name>/requirements.txt`。
- **美股侧**：institutional-flow-tracker 走 SEC 免费；earnings-calendar / value-dividend-screener 优先 FMP API（可选，设 `FMP_API_KEY`），无 key 时降级运行。
- **上下文成本**：本仓库会话每次加载这 20 个 skill 的 name+description 元数据；嫌吵可删除对应目录回退。
- **许可证**：finskills 各 skill 目录内含 Apache-2.0 LICENSE；tradermonty 为 MIT（根 LICENSE 未一并拷贝，来源见上表）。随仓库分发时保留本文件即可追溯。

## 重新同步

上游会更新，本项目为一次性快照拷贝，不自动同步。需要升级时：

1. 重新获取上游 main 分支最新代码（git clone 或 codeload tarball）。
2. 用新目录覆盖 `.claude/skills/<对应目录>`。
3. 更新本文件表格中的 commit 哈希。
