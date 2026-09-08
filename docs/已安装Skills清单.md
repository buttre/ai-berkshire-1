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
> 另：全局额外安装了 **69** 个第三方 Skill（不计入上方 20 个投研 Skill）：`convert-documents-to-markdown`、`grill-me`、mattpocock/skills×28、finance-skills×7、investorskills×30、`longbridge-value-investing`、`a-stock-data`。见文末「额外安装」。

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

### 个体 Skill（2 个）

| Skill | 名称 / 简介 | 来源 | 安装位置 | 触发 / 调用 |
|-------|-------------|------|----------|------------|
| `convert-documents-to-markdown` | 文档转 Markdown：Word(.doc/.docx)、PPT、Excel、OpenDocument、RTF、EPUB、CSV、PDF → GitHub-Flavored Markdown | anydoc（firecrawl）`anydoc-main.zip` | `~/.claude/skills/convert-documents-to-markdown/SKILL.md` | 自动触发（遇到无法直接读取的文档时）；依赖 Node 20+，经 `npx -y @firecrawl/anydoc` 调用，免预装 |
| `grill-me` | 拷问模式：逐条穷举拷问你的计划/论文，直到决策树全部分支收敛、达成共识 | RobMitt/grill-me-skill（GitHub） | `~/.claude/skills/grill-me/SKILL.md` | 自然语言触发：说 "grill me on X" 或 "压测一下我的计划/论文" |

### mattpocock/skills 批量（GitHub，2026-09-08 安装，29 个已发布）

> 来自 [github.com/mattpocock/skills](https://github.com/mattpocock/skills)，整目录安装（SKILL.md + 各 skill 自带 references/模板），统一位置 `~/.claude/skills/{skill}/`。以英文软件工程向为主，多数经自然语言/描述触发，非 `/{skill}` 命令式。跳过 in-progress 目录下 8 个未完成草稿；其中 `grill-me` 因触发名与已装 RobMitt 版相同，保留现版本未覆盖。

| 仓库目录 | 数量 | Skills |
|---------|------|--------|
| `engineering/` | 18 | `ask-matt` `code-review` `codebase-design` `diagnosing-bugs` `domain-modeling` `grill-with-docs` `implement` `improve-codebase-architecture` `prototype` `research` `resolving-merge-conflicts` `setup-matt-pocock-skills` `tdd` `to-spec` `to-tickets` `triage` `wayfinder` `wizard` |
| `productivity/` | 7 | `grill-me` `grilling` `handoff` `teach` `to-questionnaire` `wait-what` `writing-for-agents` |
| `misc/` | 4 | `git-guardrails-claude-code` `migrate-to-shoehorn` `scaffold-exercises` `setup-pre-commit` |

### finance-skills（himself65，★3299·MIT·活跃，2026-09-08 装 7 个）

> 来自 [github.com/himself65/finance-skills](https://github.com/himself65/finance-skills)，仅取其投研相关的 `plugins/market-analysis` + `plugins/data-providers`（剔除 crypto/social/UI/startup 等插件），整目录安装。英文触发。**依赖**：yfinance-data/estimate-analysis/stock-correlation 等需 Python `yfinance`；fintel-data 需 `FINTEL_API_KEY`（可走 fintel.io 官方 MCP）；finance-sentiment 走 Adanos Finance API。未装 earnings-preview/recap（与本项目 earnings-* 重复）。

| 插件 | 数量 | Skills |
|------|------|--------|
| `market-analysis` | 5 | `company-valuation` `yfinance-data` `estimate-analysis` `stock-correlation` `stock-liquidity` |
| `data-providers` | 2 | `fintel-data` `finance-sentiment` |

### investorskills（xuboyuebobb，★1842·MIT·活跃，2026-09-08 装 30 个）

> 来自 [github.com/xuboyuebobb/investorskills](https://github.com/xuboyuebobb/investorskills)，大师风格库中选取价值+成长+宏观 30 个（剔除 crypto×12、与你四大师重复的 `buffett`/`munger`/`li-lu-value`/`duanyongping`×4、初创 VC×5、纯量化/短线TA×10）。统一位置 `~/.claude/skills/{style}/`，英文描述触发。

| 风格组 | 数量 | Skills |
|--------|------|--------|
| 价值/烟蒂/集中 | 12 | `graham-net-net` `klarman-deep-value` `schloss-cigar-butt` `templeton-max-pessimism` `watsa-insurance-float` `hohn-concentrated-quality` `nick-sleep-scale-economies` `greenblatt-special-situations` `marks-cycles` `burry-asymmetric-contrarian` `danbin-longterm-compounder` `ackman-concentrated-activism` |
| 法证/做空风控 | 4 | `einhorn-forensic-short` `muddy-waters-forensic` `hindenburg-investigation` `spruce-point-accounting-short` |
| 成长 | 3 | `lynch-growth` `coleman-tiger-growth` `cathie-wood-innovation` |
| 宏观 | 8 | `dalio-principles-allweather` `soros-reflexivity` `druckenmiller` `tepper-distressed-macro` `gundlach-bonds` `libei-macro-hedge` `ptj-macro-trend` `shihanbing-macro-interest-analysis` |
| A股价值/产业 | 3 | `qiuguolu-value-quality` `zhanglei-longterm-research-value` `dengxiaofeng-cycle-industry` |

### longbridge-value-investing（长桥 Longbridge，MIT·活跃，2026-09-08 装）

> 来自 [github.com/longbridge/skills](https://github.com/longbridge/skills) 的 `longbridge-value-investing`（格雷厄姆 NCAV/net-net + 巴菲特护城河/ROE 双方法，含 4 个 references 评分模板）。触发词含 格雷厄姆/巴菲特/护城河/烟蒂/NCAV/value investing。数据优先 Longbridge CLI（可选装），MCP 兜底，WebSearch 仅补缺。兄弟 skill（earnings/fundamentals/research/quant…共 12 个）未装。

### a-stock-data（simonlin1212，★9699·Apache-2.0·活跃，2026-09-08 装）

> 来自 [github.com/simonlin1212/a-stock-data](https://github.com/simonlin1212/a-stock-data)，A股真实数据取数单技能（SKILL.md ≈175KB，自包含可运行代码、零外部依赖，覆盖行情/K线/研报/龙虎榜/两融/资金流/财务三表/公告/估值历史/宏观等 60 端点）。触发：需要写代码实际抓取 A股数据时；概念解释/观点讨论等不取数话题**不会**加载。

### 新装投资类 Skill 使用总览（39 个，2026-09-08）

> 均为描述触发型（非 `/{skill}` 命令）：直接说出你想分析的标的/问题即可，Claude 会自动套用最匹配的技能。示例按中文习惯给出，英文触发词亦可。

**finance-skills（7）— 数据层与估值**

| Skill | 使用方法 | 示例用法 |
|-------|----------|----------|
| `company-valuation` | DCF + 相对估值 + SOTP 三种方法估算内在价值，三角化出目标价区间 | "英伟达值多少钱？做个 DCF 和同业对比" |
| `yfinance-data` | 用 yfinance 拉行情/财务三表/期权/分红/分析师数据 | "拉取腾讯最近 5 年利润表与 ROE" |
| `estimate-analysis` | 分析师一致预期与修正趋势深度分析 | "英伟达的 EPS 一致预期近半年怎么被上修/下调？" |
| `stock-correlation` | 股票相关性与配对、找同族标的 | "找和英伟达相关性最高的几只股票" |
| `stock-liquidity` | 评估流动性/买卖价差/大单冲击成本 | "我 100 万港元买美团，会不会把价格打上去？" |
| `fintel-data` | 查 Fintel 空头/借券费率/13F 机构/内幕（需 `FINTEL_API_KEY`） | "拼多多最新空头比例和借券成本多少？" |
| `finance-sentiment` | 聚合 Reddit/X/新闻对个股的情绪热度 | "Reddit/X 上最近对特斯拉是热还是冷？" |

**investorskills（30）— 大师视角风格库**（做对应类型判断时，让 Claude 套用该视角）

| Skill | 使用方法 | 示例用法 |
|-------|----------|----------|
| `graham-net-net` | 评估净流动资产折扣股（net-net/烟蒂） | "扫一遍美股有没有价格低于净流动资产的美烟蒂" |
| `klarman-deep-value` | 深度价值/困境折扣、强调下行保护 | "哪些被强制卖压打低、但基本面没坏的票值得研究" |
| `schloss-cigar-butt` | 施洛斯式便宜分散捡烟蒂 | "按施洛斯方法从低估清单挑一篮子" |
| `templeton-max-pessimism` | 全球最悲观点逆向价值 | "全球市场现在哪个角落被过度悲观错杀？" |
| `watsa-insurance-float` | 保险浮存金视角 + 保守配置 | "用浮存金逻辑看伯克希尔这类公司" |
| `hohn-concentrated-quality` | 集中优质、定价权、高 ROIC | "这家高 ROIC 公司值不值得下重注？" |
| `nick-sleep-scale-economies` | 规模经济共享的长期复利（像 Nick Sleep） | "它把规模优势让利给客户、换长坡厚雪了吗？" |
| `greenblatt-special-situations` | 分拆/重组/事件驱动 + 神奇公式 | "看看有没有分拆或强制卖压造成的低估机会" |
| `marks-cycles` | 周期位置 + 风险溢价 + 第二层思维 | "现在风险溢价在周期什么位置，该攻还是守？" |
| `burry-asymmetric-contrarian` | 非对称逆向、反共识机会 | "这笔逆向交易是不是下行有限、上行不对称？" |
| `danbin-longterm-compounder` | 长期复利、穿越波动持有优质公司 | "用长期复利标准审这只核心持仓还能拿吗" |
| `ackman-concentrated-activism` | 集中重注 + 公开催化 + 激进参与 | "像 Ackman 那样评估这公司的催化与集中持仓逻辑" |
| `einhorn-forensic-short` | 会计红旗/治理问题法证分析 | "查这只票有没有财务粉饰的红旗（绿光式）" |
| `muddy-waters-forensic` | 造假链条、渠道验证、现金核验 | "用浑水方法核验这家公司现金流真实性" |
| `hindenburg-investigation` | 证据链、关联方、股权质押、做空叙事 | "按兴登堡方法查它的关联方与股权质押" |
| `spruce-point-accounting-short` | 利润质量、激进会计调整、收购会计 | "审查这笔并购的会计处理有没有粉饰利润" |
| `lynch-growth` | 林奇六类股分类 + PEG | "用林奇方法判断这是成长股还是成长陷阱" |
| `coleman-tiger-growth` | 可扩展平台、网络效应、单位经济 | "这家平台公司的单位经济模型跑得通吗？" |
| `cathie-wood-innovation` | 颠覆式创新 S 曲线、长程成长 | "评估 AI 终端这类颠覆主题的长期成长曲线" |
| `dalio-principles-allweather` | 经济机器/债务周期 + 全天候配置 | "按达利欧全天候思路看我股债现金的配比" |
| `soros-reflexivity` | 反身性、宏观错位、趋势借力 | "现在有什么反身性正反馈可能在反向破裂？" |
| `druckenmiller` | 自上而下流动性/利率宏观交易 | "当前流动性周期对哪些资产最有利？" |
| `tepper-distressed-macro` | 危机资产、政策底、资本结构 | "市场恐慌时哪些被打骨折的资产有政策托底？" |
| `gundlach-bonds` | 债券/久期/收益率曲线相对价值 | "曲线倒挂对长债仓位意味着什么？" |
| `libei-macro-hedge` | 宏观对冲、仓位与回撤风控 | "按李蓓式宏观对冲，现在该降仓还是加对冲？" |
| `ptj-macro-trend` | 大趋势确认、拐点与止损纪律 | "这轮商品趋势确认转多了吗？该不该跟？" |
| `shihanbing-macro-interest-analysis` | 利益分析法推演宏观/政策方向 | "用利益分析法推演这轮政策谁受益、钱往哪流" |
| `qiuguolu-value-quality` | 能力圈 + 行业龙头结构性优势 | "邱国鹭式：这行业龙头的结构性优势在哪？" |
| `zhanglei-longterm-research-value` | 长期研究驱动、做时间的朋友 | "张磊式：这门生意是不是时间的朋友？" |
| `dengxiaofeng-cycle-industry` | 周期位置 + 产业链 + 底部买龙头 | "邓晓峰式：这行业周期到哪了，龙头见底没？" |

**longbridge + a-stock（2）**

| Skill | 使用方法 | 示例用法 |
|-------|----------|----------|
| `longbridge-value-investing` | 格雷厄姆 NCAV/net-net + 巴菲特护城河双方法：单股诊断或批量筛选（数据优先 Longbridge CLI/MCP，无则 WebSearch） | "捡烟蒂：用 net-net 扫一遍 A 股+美股低估标的" 或 "给 XX 做护城河/ROE 价值投资评分" |
| `a-stock-data` | 写代码实际抓取 A 股真实数据（行情/K线/财务三表/龙虎榜/两融/资金流/估值史/宏观，60 端点自包含） | "用代码抓取宁德时代近 3 年财务三表和最新北向持仓" |

> 说明：均为非本项目投研 Skill，不计入上方 20 个与分类统计。凡在本环境全局安装的第三方/额外 Skill，一律记录于本表。
