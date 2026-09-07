# AI Berkshire 已安装 Skills 清单

> 生成日期：2026-09-07
>
> 本项目共 **20** 个投研 Skill，均已安装到本地 Claude 环境，三处位置内容一致：
> - 仓库源码：`skills/{skill}.md`
> - 安装副本 1：`~/.claude/commands/{skill}.md`
> - 安装副本 2：`~/.claude/skills/{skill}/SKILL.md`
>
> 调用方式：在 Claude Code 中输入 `/{skill}` 并跟上参数（如 `/investment-research 腾讯`）。
>
> 另：全局额外安装了 **2** 个第三方 Skill（`convert-documents-to-markdown`、`grill-me`，均非本项目投研 Skill），见文末「额外安装」。

## 总览表

| # | Skill | 名称 / 简介 | 分类 | 输入格式示例 | 使用说明 | 使用示例 | 参考输出文件 |
|---|-------|-------------|------|-------------|----------|----------|-------------|
| 1 | `bottleneck-hunter` | 供应链瓶颈猎手：AI 驱动的全球产业链瓶颈套利 | 行业与筛选 | 超级趋势（如 `AI算力`） | 认准一个 3-5 年确定性的超级趋势后，扫供应链"哪一环会先不够用"，挖第二/三层瓶颈的套利标的 | `/bottleneck-hunter AI算力` | 漏斗/套利研究底稿 |
| 2 | `deep-company-series` | 看懂 XX 公司（深度公司系列）：3-8 篇长文拆一家公司 | 内容与问答 | 公司名 | 为一家公司做教科书级深度研究，以 3-8 篇系列长文公开发布（单篇研报请用 research/earnings） | `/deep-company-series 腾讯` | `reports/{公司名}/《看懂{公司名}》/` |
| 3 | `dyp-ask` | 段永平问答：以他的方式思考（角色模拟） | 内容与问答 | 任意投资/人生问题 | 模拟段永平本人，用"本分/平常心/做对的事情"的思维回答你的问题 | `/dyp-ask 怎么看待能力圈以外的机会` | 对话输出 |
| 4 | `earnings-review` | 财报精读：一手资料深度解读 | 个股研究 | `公司名 季度`（如 `腾讯 2025Q4`） | 财报发布后精读一手资料（年报/季报/电话会），不做二手研报解读 | `/earnings-review 腾讯 2025Q4` | `reports/{公司名}/{公司名}-earnings-{期间}.md` |
| 5 | `earnings-team` | 财报精读团队：四大师并行解读 + 公众号发布 | 个股研究 | `公司名 季度` | 与 earnings-review 同场景，但要四大师并行 + 编辑润色，产出可直接发布的公众号文章 | `/earnings-team 美团 2025年报` | `reports/{公司名}/{公司名}-earnings-{期间}.md`（公众号定稿） |
| 6 | `financial-data` | 财务数据获取与交叉验证规范 | 数据与工具 | 无（规范类，供其他 Skill 引用） | 规定美股/港股/A股/台股的数据源与双源交叉验证规则，被其他投研 Skill 自动引用 | 无需直接调用；需要时在对话中引用，如"用 financial-data 规范核对" | — |
| 7 | `income-investment` | Income Investment：Durable and Opportunistic Distribution Analysis | 个股研究 | 公司名（英文 Skill） | 判断公司分红/分配收入的持久性与吸引力，适合长期收入仓还是机会型收益仓（英文产出） | `/income-investment "台积电" role=core-income tax_residence=US` | 分红能力/收益持仓研究 |
| 8 | `industry-funnel` | 行业漏斗筛选：从全市场到 3 家的价值投资精选流程 | 行业与筛选 | 行业/方向（如 `AI算力`） | 对某行业从全市场逐层筛到 3 家终选，每层留/弃理由可追溯；可与 industry-research 互补 | `/industry-funnel 创新药` | `reports/{行业}-funnel-{YYYYMMDD}.md` |
| 9 | `industry-research` | 行业投资研究：产业链全景扫描 + 四大师个股分析框架 | 行业与筛选 | 行业/主题 | 做产业链全景研究：验证逻辑链 → 画全景图 → 扫全球上市公司 → 环节头部四大师分析 | `/industry-research AI算力` | `reports/{行业}-industry-{YYYYMMDD}.md` |
| 10 | `investment-checklist` | 巴菲特价值投资买入前 Checklist | 个股研究 | 公司名（支持多家，逗号/空格分隔） | 买入决策前的六关检查清单，目的是排除坏选择；支持多家并行对比 | `/investment-checklist 腾讯, 茅台` | `reports/{公司名}/{公司名}-checklist-{YYYYMMDD}.md` |
| 11 | `investment-research` | 投资研究：巴菲特-芒格-段永平-李录 四大师综合分析框架 | 个股研究 | 公司名 | 单家上市公司的标准系统化投研（七模块），产出独立研究报告，是各深度 Skill 的地基 | `/investment-research 美团` | `reports/{公司名}/{公司名}-research-{YYYYMMDD}.md` |
| 12 | `investment-team` | 投研团队：四角色并行分析框架 | 个股研究 | 公司名 | 需要更深/更广视角时，用多 Agent 并行团队（商业/财务/行业/风险四角色）研究一家公司 | `/investment-team 英伟达` | `reports/{公司名}/`（4 视角 + 最终报告） |
| 13 | `management-deep-dive` | 管理层纵深研究：买股票就是买人 | 个股研究 | `人名 公司名`（如 `王兴 美团`） | 当标准投研中管理层评分 ≤★★★ 或管理层是核心逻辑时，纵深研究人（话vs做、资本配置、品格） | `/management-deep-dive 王兴 美团` | `reports/{公司名}/{公司名}-management-{YYYYMMDD}.md` |
| 14 | `news-pulse` | 公司新闻脉搏：股价异动快速归因团队 | 数据与工具 | 公司名 | 持仓股大涨大跌（单日 ±5%/一周 ±10%）或重大新闻时，10 分钟快速归因并判断是否触发论文重审 | `/news-pulse 腾讯` | 事件时间线 + 异动主因 + 是否触发论文重审 |
| 15 | `portfolio-review` | 组合管理：从"研究公司"到"管理组合" | 持仓与纪律 | 持仓清单或 `我的持仓` | 组合层体检：集中度/相关性/机会成本/压力测试 → 调仓建议；建议每季度审视一次，勿过度交易 | `/portfolio-review 腾讯30%, 美团20%, 茅台20%, 现金30%` 或 `/portfolio-review 我的持仓` | `reports/portfolio-latest.md` |
| 16 | `private-company-research` | 未上市公司研究：多 Agent 并行深度研究框架 | 个股研究 | 公司名（如 `蚂蚁集团`、`SpaceX`） | 对蚂蚁、SpaceX 等未上市公司用多源拼图式研究还原生意真实价值，所有数据标注置信度 | `/private-company-research 蚂蚁集团` | `reports/{公司名}/{公司名}-private-{YYYYMMDD}.md` |
| 17 | `quality-screen` | 去劣筛选：7 条指标快速排除非一流公司 | 行业与筛选 | 公司名或标的清单 | 研究前的第一道过滤器：7 条硬指标 + 豁免规则，快速剔除非一流公司（支持行业/指数/主题批量） | `/quality-screen 恒生指数成分股` | 去劣打分底稿 |
| 18 | `thesis-drift` | 投资论文漂移检测：分清事实变化与措辞变化 | 持仓与纪律 | `公司名 旧报告 新报告` 或公司名 | 新旧论文/报告对比，区分事实/价格/措辞三种变化，只在证据变时承认论文漂移 | `/thesis-drift 腾讯 腾讯-thesis-20260101.md 腾讯-thesis-20260701.md` | 漂移检测报告 |
| 19 | `thesis-tracker` | 投资论文追踪：买入后的纪律系统 | 持仓与纪律 | 公司名（或 `公司名 季度检查`） | 买入后纪律：首次建立投资论文（含卖出条件/红线），之后季度检查论文是否仍完整 | `/thesis-tracker 腾讯 季度检查` | `reports/{公司名}/{公司名}-thesis.md` |
| 20 | `wechat-article` | 微信公众号文章：作者-编辑-读者三 Agent 协作 | 内容与问答 | 主题描述 | 把一个主题/论文深挖成可直接发布的公众号文章（作者写、编辑修、读者审三 Agent） | `/wechat-article 为什么巴菲特不买科技股` | 可直接发布的公众号文章 |

## 分类速览

| 分类 | 数量 | Skills |
|------|------|--------|
| 个股研究 | 8 | `earnings-review` `earnings-team` `income-investment` `investment-checklist` `investment-research` `investment-team` `management-deep-dive` `private-company-research` |
| 行业与筛选 | 4 | `bottleneck-hunter` `industry-funnel` `industry-research` `quality-screen` |
| 持仓与纪律 | 3 | `portfolio-review` `thesis-drift` `thesis-tracker` |
| 内容与问答 | 3 | `deep-company-series` `dyp-ask` `wechat-article` |
| 数据与工具 | 2 | `financial-data` `news-pulse` |

> 说明：分类为便于检索的速览分组，Skill 的实际触发方式与输出路径以 `skills/` 源码正文及 `CLAUDE.md` 报告命名规范为准。

## 额外全局 Skill（非投研）

| Skill | 名称 / 简介 | 来源 | 安装位置 | 触发 / 调用 |
|-------|-------------|------|----------|------------|
| `convert-documents-to-markdown` | 文档转 Markdown：Word(.doc/.docx)、PPT、Excel、OpenDocument、RTF、EPUB、CSV、PDF → GitHub-Flavored Markdown | anydoc（firecrawl）`anydoc-main.zip` | `~/.claude/skills/convert-documents-to-markdown/SKILL.md` | 自动触发（遇到无法直接读取的文档时）；依赖 Node 20+，经 `npx -y @firecrawl/anydoc` 调用，免预装 |
| `grill-me` | 拷问模式：逐条穷举拷问你的计划/论文，直到决策树全部分支收敛、达成共识 | RobMitt/grill-me-skill（GitHub） | `~/.claude/skills/grill-me/SKILL.md` | 自然语言触发：说 "grill me on X" 或 "压测一下我的计划/论文" |

> 说明：均为非本项目投研 Skill，不计入上方 20 个与分类统计。凡在本环境全局安装的第三方/额外 Skill，一律记录于本表。
