# 本项目投研 Skills 清单

> 更新日期：2026-09-09
>
> 项目含 **20 个投研 Skill**（`skills/*.md` 为 Claude Code command 源文件，本机 `~/.claude/commands/` 已安装其中 19 个）。`codex-skills/` 是给 Codex 客户端生成的同一套工作流（21 个，多 `investment-memo-craft`）。

## 使用方式

在 Claude Code 中输入 `/skill名称 参数` 即可调用，例如 `/investment-research 腾讯`。每个 Skill 支持的具体输入格式见下表「用法」列，输出报告写入 `reports/` 目录。

## Skills 一览表

| # | Skill | 作用 | 用法（`/skill 参数`） | 报告输出 |
|---|-------|------|----------------------|----------|
| 1 | **/investment-research** | 四大师（巴菲特-芒格-段永平-李录）综合投研 | `/investment-research 腾讯` | `reports/{公司}/` 或根目录 `{公司}-research-YYYYMMDD.md` |
| 2 | **/investment-team** | 四角色多 Agent 并行团队研究 | `/investment-team 美团` | `reports/{公司}/` 四视角+最终报告 |
| 3 | **/investment-checklist** | 巴菲特买入前 Checklist | `/investment-checklist 茅台, 英伟达, 苹果` | `reports/{公司}-checklist-YYYYMMDD.md` |
| 4 | **/management-deep-dive** | 管理层纵深研究（"买股票就是买人"） | `/management-deep-dive 王兴 美团` | `reports/{公司}-management-YYYYMMDD.md` |
| 5 | **/earnings-review** | 财报精读（只读一手财报） | `/earnings-review 腾讯 2025Q4` | `reports/{公司}-earnings-{期间}.md` |
| 6 | **/earnings-team** | 财报精读团队：四大师解读+编辑+读者评审→公众号定稿 | `/earnings-team PDD 2025年报` | `reports/{公司}/`（公众号定稿） |
| 7 | **/financial-data** | 财务数据取数与交叉验证规范（两个独立来源、误差>1%须标记） | 被各 skill 调用；也可 `/financial-data 腾讯` | 规范文档 |
| 8 | **/industry-research** | 行业产业链全景扫描+四大师个股分析 | `/industry-research 核电` | `reports/{行业}-industry-YYYYMMDD.md` |
| 9 | **/industry-funnel** | 行业漏斗筛选：全市场逐层精选到 3 家终选 | `/industry-funnel AI算力` | `reports/{行业}-funnel-YYYYMMDD.md` |
| 10 | **/quality-screen** | 去劣筛选：7 条指标排除非一流公司 | `/quality-screen 恒生指数成分股` | 根目录筛选报告 |
| 11 | **/bottleneck-hunter** | 供应链瓶颈扫描与套利机会挖掘（找"先不够用"的一环） | `/bottleneck-hunter AI基础设施` | 根目录 |
| 12 | **/portfolio-review** | 投资组合审视与优化 | `/portfolio-review 腾讯30%, 美团20%, 茅台20%, 现金30%` | `持仓与交易/portfolio-latest.md` |
| 13 | **/income-investment** | 股息收入投资分析（**仓库有、本机未安装**） | `/income-investment Verizon mode=existing role=core-income quantity=100 cost_basis=39.50 tax_residence=France horizon=5y` | 根目录 |
| 14 | **/thesis-tracker** | 买入后论文纪律系统（建论文/季度检查） | `/thesis-tracker 拼多多` | `reports/{公司}-thesis.md` |
| 15 | **/thesis-drift** | 投资论文漂移检测（区分事实变化与措辞变化） | `/thesis-drift 拼多多 <旧路径> <新路径>` | 根目录 |
| 16 | **/news-pulse** | 股价异动快速归因（4 Agent：事件/政策/对手/情绪，10分钟出结论） | `/news-pulse 腾讯` | 根目录 |
| 17 | **/private-company-research** | 未上市公司深度研究（蚂蚁/SpaceX/小红书等） | `/private-company-research SpaceX` | `reports/{公司}-private-YYYYMMDD.md` |
| 18 | **/deep-company-series** | 《看懂XX》深度长文系列（3-8 篇，公众号发布） | `/deep-company-series 拼多多` | `reports/{公司}/《看懂{公司》/` |
| 19 | **/wechat-article** | 公众号文章：作者-编辑-读者三 Agent 协作 | `/wechat-article 美团` | 根目录 |
| 20 | **/dyp-ask** | 扮演段永平本人问答 | `/dyp-ask 拼多多的护城河到底在哪里？` | 对话输出 |

## 快速分类入口

- **深度研究**：`/investment-research`（单家）→ `/investment-team`（团队并行）→ `/investment-checklist`（买入前把关）
- **财报分析**：`/earnings-review`（单篇精读）→ `/earnings-team`（团队版、可发布）
- **行业筛选**：`/industry-research`（全景）→ `/industry-funnel`（漏斗精选）→ `/quality-screen`（去劣）→ `/bottleneck-hunter`（瓶颈套利）
- **持仓管理**：`/thesis-tracker` + `/news-pulse` + `/thesis-drift` + `/portfolio-review`
- **内容创作**：`/deep-company-series` + `/wechat-article`
- **思维工具**：`/dyp-ask`

## 三点说明

- **安装状态**：本机 `~/.claude/commands/` 已安装 19 个，缺 **income-investment**（仓库 `skills/` 里有，但未安装）。安装命令：`.\scripts\install-claude-commands.bat`（Windows）或 `./scripts/install-claude-commands.sh`（macOS/Linux）。
- **Codex 版**：`codex-skills/` 是同一套工作流为 Codex 客户端生成的包（21 个，多一个 `investment-memo-craft`），与 `codex-prompts/` 配套，由 `scripts/sync-codex-skills.py` 从 `skills/*.md` 生成。
- **非本项目自带**：环境内另有 harness 内置 Skill（`browser-act` 浏览器自动化、`dataviz` 图表、`claude-api`、`/run`、`/init`、`/security-review` 等），不属于本仓库安装范围。
