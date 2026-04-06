---
name: obsidian-kb-internalize
description: "当用户希望把 D:\\Nutstore\\Obsidian 下资料自动处理、处理、变成wiki、wiki化、内化为 Obsidian 知识库时使用。执行一键管线：ingest、compile、health，并可按问题追加 ask 或 render 输出。采用 LLM-first 编译策略（尽量少规则）。"
---

# Obsidian KB Internalize

## Use When
- 用户说“请帮我自动处理”“处理”“变成wiki”“wiki”“内化”。
- 用户想把 `D:\Nutstore\Obsidian` 或其子目录的资料编译成结构化 Wiki。
- 用户希望在编译后自动做问答、健康检查或生成汇报材料。

## Defaults
- Vault: `D:\Nutstore\Obsidian`
- Raw source: `D:\Nutstore\Obsidian`（默认只摄取 Markdown）
- KB engine: `D:\Nutstore\Obsidian\Coding\obsidian-kb-engine\kb.py`
- Default project: `main-wiki`
- Default LLM endpoint: `https://openrouter.ai/api/v1`
- Default model: `qwen/qwen3.6-plus:free`
- Default API key env: `OR_API_KEY`（可通过 `--api-key-env` 覆盖）
- Prompt version: `2026-04-05-llm-first-v5`
- Summary max chars: `3600`
- Concepts per doc: `8`
- Concept min source count: `3`（更严格，减少噪声概念）
- QA top_k: `6` / QA context chars: `1200` / QA max tokens: `1200`（更快）

更多路径与参数见 [references/defaults.md](references/defaults.md)。

## Workflow
1. 先运行一键脚本完成基础管线。
2. `compile` 后默认自动执行 `conceptdef`（用 LLM 写概念定义）。
3. 若用户给了具体问题，再追加 QA。
4. 若用户提到“汇报/幻灯片/Marp/图表”，再追加 render。
5. 最后回报输出路径（Wiki index、QA、Health、Slides、Figures、Conceptdef）。

## Command
先看帮助：
```powershell
python C:\Users\Administrator\.codex\skills\obsidian-kb-internalize\scripts\run_internalize.py --help
```

常用执行（基础一键）：
```powershell
python C:\Users\Administrator\.codex\skills\obsidian-kb-internalize\scripts\run_internalize.py --project main-wiki --api-key "<YOUR_KEY>"
```

基于已有 `raw/` 仅重编译（不再摄取）：
```powershell
python C:\Users\Administrator\.codex\skills\obsidian-kb-internalize\scripts\run_internalize.py --project main-wiki --raw-source D:\Nutstore\Obsidian\main-wiki\raw --skip-ingest
```

带问答：
```powershell
python C:\Users\Administrator\.codex\skills\obsidian-kb-internalize\scripts\run_internalize.py --project main-wiki --ask "这个主题最关键的3个结论是什么？"
```

带渲染：
```powershell
python C:\Users\Administrator\.codex\skills\obsidian-kb-internalize\scripts\run_internalize.py --project main-wiki --render "请生成可汇报版本"
```

自动回答“待追问”并输出到 `outputs/待追问`：
```powershell
python C:\Users\Administrator\.codex\skills\obsidian-kb-internalize\scripts\run_internalize.py --project main-wiki --followup
```

自动生成概念页定义（LLM 写入 `wiki/concepts`）：
```powershell
python C:\Users\Administrator\.codex\skills\obsidian-kb-internalize\scripts\run_internalize.py --project main-wiki --concept-define
```

## Execution Rules
- 先做“问题分型”，再决定是否需要重编译：
  - 仅 `conceptdef` 失败：只跑 `conceptdef`，禁止直接 `--full-compile`。
  - 仅 `health` 异常（断链/候选问题）：只跑 `health`。
  - 仅 QA/followup 输出异常：只跑对应子命令（`ask` / `followup`）。
  - 只有在提示词版本变更、编译参数大改、或源文件大规模变化时，才允许 `--full-compile`。
- 默认使用 `--project main-wiki`，除非用户明确指定项目名。
- 默认源目录固定 `D:\Nutstore\Obsidian`，并开启仅 Markdown 摄取。
- 若需摄取非 Markdown，追加 `--all-formats`。
- 若只想基于当前项目 `raw/` 重跑，使用 `--skip-ingest`（或把 `--raw-source` 指向该项目 `raw/`，会自动跳过 ingest）。
- 若仅需跑问答/待追问而不重新编译，使用 `--skip-compile`（最快）。
- 如需覆盖模型配置，使用 `--base-url` 和 `--model`。
- 如需切换鉴权变量（如 `OPENAI_API_KEY` / `OR_API_KEY`），使用 `--api-key-env`。
- 如需微调 LLM-first 编译行为，使用 `--timeout-seconds`、`--summary-max-chars`、`--concepts-per-doc`、`--prompt-version`。
- 如需自动生成“待追问”答案，追加 `--followup`，并可用 `--followup-max-per-source`、`--followup-max-sources` 控制规模。
- 如需进一步提速，调小 `--followup-top-k`、`--qa-context-chars`、`--qa-answer-max-tokens`。
- 默认会在 `compile` 后自动跑概念定义生成；如需跳过，使用 `--skip-concept-define`。
- 如需在 `--skip-compile` 场景下也强制生成概念定义，追加 `--concept-define`；可用 `--concept-define-max`、`--concept-define-min-source`、`--concept-define-batch-size`、`--concept-define-overwrite` 控制范围。
- 如果源目录不存在或为空，先告知用户并停止。
- 发生命令失败时，直接返回失败命令和 stderr 关键行。
- 不改写用户已有笔记；输出只写到 `<vault-root>/<project>/`。

