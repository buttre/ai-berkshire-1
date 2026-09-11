
- **refine** `1789115835` prompt_note `h_c53dc432e83c4032b29a663233512837`
  - title: skills/*.md 改动需同步 Codex 与 Claude 两侧生成物
  - content: `skills/*.md` 是唯一的 canonical workflow 源（Claude Code 斜杠命令格式，正文用 `$ARGUMENTS`，多数无 frontmatter）。改动后有三个下游需要同步：
- `python3 scripts/sync-codex-skills.py`（生成 codex-skills/*/SKILL.md，含 Codex adapter note）
- `python3 scripts/sync-codex-prompts.py`（生成 codex-prompts/*.md）
- `python scripts/sync-claude-skills.py`（生成 .claude/skills/<name>/SKILL.md，含中文适配说明；支持 --show NAME 预览单个）

每个都支持 `--check`（只读校验，CI 友好）。Windows 上 Python 输出含 emoji 的源文件到控制台会触发 GBK 编码错误，脚本内需 reconfigure stdout 为 utf-8。另外 `~/.claude/commands/` 的安装方式是 `copy /Y skills/*.md`（scripts/install-claude-commands.bat），只增不删，源新增文件后必须重跑才会补上。
  - evidence: 2026-09-11 实现 sync-claude-skills.py 时确认：脚本首次运行时 `--show` 因 Windows GBK 控制台无法编码源文件里的 ❌/🔴 emoji 而崩溃，加 sys.stdout.reconfigure(encoding="utf-8") 后正常。同时实测 `sync-codex-skills.py --check` 报 codex-skills/investment-research/SKILL.md 过期，`~/.claude/commands/` 缺 income-investment.md 且 investment-research.md 与源 SHA256 不一致——两者都是"源改了但下游没重跑"。
