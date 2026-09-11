# 第三方投研 Skills 使用清单

> 更新日期：2026-09-09
>
> 本次安装的 20 个社区投研 skill，位于项目级 `.claude/skills/`。**调用方式与 ai-berkshire 自带 `/command` 不同**：这些是 SKILL.md 格式，不需要打 `/xxx`，直接用**自然语言描述需求**，Claude 会按描述自动调用对应 skill（也可在输入框直接点名 skill 名）。
>
> 上游来源/许可证/取舍见 [skills-第三方来源.md](skills-第三方来源.md)；自有 command 用法见 [skills-清单.md](skills-清单.md)。

## 分组速览

- **A股实时数据**：findata-toolkit-cn（其余 A股 skill 分析时会引用它取数）
- **A股筛选**：undervalued-stock-screener、high-dividend-strategy、quant-factor-screener、small-cap-growth-identifier、event-driven-detector、insider-trading-analyzer、sentiment-reality-gap、esg-screener
- **A股单公司/板块深度**：financial-statement-analyzer、tech-hype-vs-fundamentals
- **A股组合/宏观**：portfolio-health-check、risk-adjusted-return-optimizer、sector-rotation-detector、suitability-report-generator
- **美股**：institutional-flow-tracker（13F）、earnings-calendar、us-stock-analysis、value-dividend-screener、finviz-screener

## 使用清单（finskills · A股）

| # | Skill 目录 | 作用（触发场景） | 使用示例 |
|---|-----------|------------------|----------|
| 1 | **findata-toolkit-cn** | A股数据工具：实时行情、财务指标、董监高增减持、北向资金、宏观（LPR/CPI/PPI/PMI/社融/M2）。免费免 API key | 「用 findata 拉贵州茅台近5年财务指标和最新北向资金」「查今天的 LPR 和 M2」 |
| 2 | **undervalued-stock-screener** | 扫描 A股，筛基本面强劲但低估的公司（低 PE/PB、高 ROE） | 「筛出 A股 中 PE<15、ROE>15% 的低估公司」 |
| 3 | **high-dividend-strategy** | A股高股息策略：分红可持续性、现金分红覆盖率、中证红利成分股、股息率排名 | 「分析中证红利里股息率>5% 且分红覆盖良好的股票」「XX 的分红能持续吗」 |
| 4 | **quant-factor-screener** | 多因子打分筛选（价值/动量/质量/低波动/规模/成长） | 「用质量+低波动因子从沪深300里打分，筛前30」 |
| 5 | **small-cap-growth-identifier** | 小市值高成长、专精特新发现 | 「筛出市值<100亿、营收增速>30% 的专精特新 A股」 |
| 6 | **event-driven-detector** | 事件驱动机会：并购重组、资产注入、回购增持、管理层变更、指数调整 | 「最近有哪些 A股 回购增持，评估套利空间」「XX 国企改革重组事件分析」 |
| 7 | **insider-trading-analyzer** | 董监高及重要股东增减持行为与信心信号 | 「找近3个月董监高净增持最多的 A股 公司」「XX 管理层近期减持怎么看」 |
| 8 | **sentiment-reality-gap** | 逆向投资：被过度看空/错杀但基本面稳健的机会 | 「找 A股 里超跌错杀、但业绩依旧稳健的公司」 |
| 9 | **esg-screener** | ESG（环境/社会/治理）筛选与评估、争议事件筛查、排除清单 | 「剔除煤炭烟草后，筛出 ESG 评分最高的 A股」「给宁德时代做 ESG 评估」 |
| 10 | **financial-statement-analyzer** | 单只 A股财报法证深挖：盈利质量、造假风险（Z/M 值）、杜邦、营运资本 | 「对贵州茅台 2025 年报做财务报表法证分析，查 Z 值」「XX 的盈利质量如何」 |
| 11 | **tech-hype-vs-fundamentals** | 科技股估值泡沫 vs 基本面（科创板/创业板、AI/芯片/新能源板块） | 「科创板 AI/芯片估值是不是泡沫」「对比寒武纪的炒作与基本面」 |
| 12 | **portfolio-health-check** | 现有组合健康诊断：集中度、相关性、因子暴露、压力测试 | 「我持仓：腾讯30%、茅台25%、比亚迪20%、现金25%，帮我审查组合风险」 |
| 13 | **risk-adjusted-return-optimizer** | 按资金/风险偏好/期限构建夏普最优 A股 组合 + 再平衡 | 「我有 100 万、3年、中风险，构建 A股 组合并给再平衡策略」 |
| 14 | **sector-rotation-detector** | 宏观+经济周期→行业轮动，6–12 个月行业超配/低配判断 | 「当前宏观下，未来半年 A股 哪些行业超配、哪些低配」 |
| 15 | **suitability-report-generator** | 机构级投资适当性报告（投资理由、风险披露、适当性评估） | 「为我对贵州茅台的投资出一份适当性报告」 |

## 使用清单（tradermonty · 美股）

| # | Skill 目录 | 作用（触发场景） | 使用示例 |
|---|-----------|------------------|----------|
| 16 | **institutional-flow-tracker** | 美股 13F 机构持仓动向："smart money" 增减仓、发现异动先机 | 「用 institutional-flow-tracker 看最近基金在增持还是减持 NVDA」 |
| 17 | **earnings-calendar** | 未来一周美股财报日历（市值>20亿美元公司，含 EPS/营收预期） | 「未来一周有哪些大盘股发财报，列个日历表」 |
| 18 | **us-stock-analysis** | 单只美股综合：基本面+技术面+同行对比+投资报告 | 「analyze AAPL」「compare TSLA vs NVDA」「给 Microsoft 出一份分析报告」 |
| 19 | **value-dividend-screener** | 美股价值+股息两段筛选：PE<20/PB<2、股息率≥3%、三年持续增长 | 「筛出 PE<20、股息率>3% 且三年稳定增长的美股」 |
| 20 | **finviz-screener** | 自然语言→FinViz 筛选条件 URL 并在浏览器打开 | 「Find oversold large caps with high ROE」「高股息成长小型股」 |

## 依赖与准备（首次使用前）

- **A股（1–15）**：多数分析 skill 会引用 findata-toolkit-cn 取数，需要 Python + AKShare。先装一次：
  ```bash
  pip install -r .claude/skills/findata-toolkit-cn/requirements.txt
  ```
- **美股（16、17、19）**：institutional-flow-tracker / earnings-calendar / value-dividend-screener 优先用 Financial Modeling Prep，设环境变量可解锁完整数据：
  ```bash
  export FMP_API_KEY=你的key   # 不设则降级或提示
  ```
  19 可选 FinViz：`FINVIZ_API_KEY`。
- **us-stock-analysis（18）**：走 Web 搜索取实时行情，无需 key。
- **finviz-screener（20）**：公共版免 key；有 Elite key 自动增强。

## 说明

- **调用即触发**：直接描述需求即可，不必记目录名；描述与某个 skill 的 description 匹配时自动调用。
- **数据合规**：finskills 面向 A股、免费源；分析结果用于研究决策参考，非投资建议。
- **卸载回退**：删除 `.claude/skills/<对应目录>/` 即失效，不影响 ai-berkshire 自带 command。
