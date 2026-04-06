# Defaults

## Fixed Paths
- Vault root: `D:\Nutstore\Obsidian`
- Raw source: `D:\Nutstore\Obsidian` (Markdown only by default)
- Engine root: `D:\Nutstore\Obsidian\Coding\obsidian-kb-engine`
- CLI entry: `D:\Nutstore\Obsidian\Coding\obsidian-kb-engine\kb.py`
- Default base URL: `https://coding.dashscope.aliyuncs.com/v1`
- Default model: `qwen3.5-plus`
- Prompt version: `2026-04-05-llm-first-v4`
- Summary max chars: `3600`
- Concepts per doc: `8`
- Concept min source count: `3`
- QA top_k/context chars/max tokens: `6 / 1200 / 1200`

## Main Outputs
- Project root: `D:\Nutstore\Obsidian\<project>`
- Wiki index: `...\wiki\Wiki-Index.md`
- QA: `...\outputs\qa\*.md`
- Health: `...\outputs\health\*.md`
- Slides: `...\outputs\slides\*.marp.md`
- Figures: `...\outputs\figures\*.png`

## Pipeline Semantics
- `init`: 项目初始化（幂等）
- `ingest`: 从源目录拷贝到项目 `raw/`（增量，默认仅 Markdown）
- `compile`: 生成来源摘要 + 概念页 + 索引
- `conceptdef`: 默认在 `compile` 后自动执行，用 LLM 批量生成/更新概念页定义
- `health`: 断链、缺失摘要、重复概念、候选问题
- `ask` / `render`: 按需生成问答与汇报材料

## Troubleshooting
- 如果 `kb.py` 不存在，先确认引擎目录是否被移动。
- 如果 `matplotlib` 缺失，`render` 会跳过 PNG 图。
- 如果没设置 `OPENAI_API_KEY`，系统会降级为无 LLM 模式（仍可检索与归档）。
