# Claude Code Skills 分享

> 本仓库收集整理我在使用 Claude Code 过程中积累的 Skills，希望能帮助更多人提升 AI 辅助创作的效率。

## 简介

Claude Code 的 Skills 系统让复杂任务变得简单。这里分享的都是我在实际使用中验证过的技能和工作流。

## 目录结构

```
claude-code-skills/
├── articles/           # 相关文章
├── skills/             # Skills 文件
│   └── wechat-publisher/   # 微信公众号发布工具
│       ├── skill.md
│       └── templates/
│           └── community-engagement.ts
│   ├── obsidian-kb-internalize/   # Obsidian 知识库内化一键管线
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── references/
│   └── refine-markdown-to-qa/     # Markdown 转高质量问答
│       ├── SKILL.md
│       └── scripts/
└── README.md
```

## 可用 Skills

### 1. WeChat Publisher - 公众号发布助手

**功能**：
- Markdown 转 微信公众号兼容 HTML
- 内置 Newsprint 学术风格样式
- 社区互动模块（改进建议 + 福利分享 + 号召参与）

**使用方式**：
```bash
cd skills/wechat-publisher
npx tsx publish-agi-newsprint.ts
```

### 2. Obsidian KB Internalize - 知识库内化编译管线

**功能**：
- 面向 `D:\Nutstore\Obsidian` 的增量内化流程
- 一键串联 `ingest`、`compile`、`conceptdef`、`health`
- 支持追问 `ask` 与汇报 `render`
- 默认采用 LLM-first 编译策略与模型池配置

**使用方式**：
```bash
python C:\Users\Administrator\.codex\skills\obsidian-kb-internalize\scripts\run_internalize.py --help
```

### 3. Refine Markdown to QA - Markdown 问答化

**功能**：
- 批量读取目录内 Markdown 文件并转换为问答形式
- 逐文件调用模型增强逻辑、上下文衔接与解释深度
- 支持处理后归档原文件

**使用方式**：
```bash
python skills/refine-markdown-to-qa/scripts/refine_markdown_to_qa.py --help
```

---

## 社区互动模块

每次发布文章时，可以在末尾自动添加：
- 🎁 本次用到的 Skills 福利分享
- 🔮 可以改进的地方
- 🙌 号召社区参与

使用示例：
```typescript
import { generateCommunitySection } from './templates/community-engagement';

const html = generateCommunitySection({
  githubUrl: 'https://github.com/kevinsong0/claude-code-skills',
  skillsUsed: [
    { name: '📰 News Aggregator', desc: '28+ 信源聚合', installCmd: 'openskills install' }
  ]
});
```

---

## 相关文章

- [用 Claude Code 写公众号文章：从研究到排版的全流程](./articles/用Claude_Code写公众号文章.md)

---

## 欢迎贡献

- ⭐ Star 支持
- 🍴 Fork 后自定义你的版本
- 🐛 提 Issue 反馈问题
- 🔀 发 PR 贡献新功能

---

## 联系方式

- GitHub: [@kevinsong0](https://github.com/kevinsong0)
- 公众号：硬核的侃爷

---

*持续更新中...*
