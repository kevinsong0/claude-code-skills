# 用 Claude Code 写公众号文章：从研究到排版的全流程

> 本文记录了使用 Claude Code 完成「AGI 实现指标的数学形式化研究」一文的完整过程，以及如何用 AI 自动解决公众号排版难题。

---

## 一、缘起：一个问题引发的研究

事情要从一次对话说起。

我在和 Claude Code 交流时，提出了一个问题：「人类如何衡量向 AGI 迈进的进展？能否将这个问题转化为数学问题？」

这个问题看似简单，却触及了人工智能研究的核心。Claude Code 立即启动了它的「search-mode」，并行派出多个专业 Agent 进行深度搜索。

### 使用的 Skills

整个研究过程中，Claude Code 调用了多个 Skills：

| Skill | 用途 |
|-------|------|
| **search-mode** | 全面搜索 AGI 相关资料 |
| **analyze-mode** | 深度分析和综合 |
| **librarian agent** | 搜索学术论文和框架 |
| **oracle agent** | 提供数学框架建议 |
| **explore agent** | 探索本地项目结构 |

这些 Agent 并行工作，在短时间内就完成了：
- Legg-Hutter 通用智能定义（2007）
- Chollet 智力度量与 ARC-AGI 基准测试
- DeepMind 六级 AGI 分类框架
- OpenAI 五级能力框架
- Bengio 等人（2025）CHC 10 维度框架
- 北京大学 (C,U,V) 框架
- 双预测性理论和 SMGI 结构理论

最终形成了一份完整的数学形式化研究报告，保存在 `D:\Obsidian\AGI实现指标的数学形式化研究.md`。

---

## 二、研究核心成果

### 核心结论

$$\boxed{\text{AGI} = \mathbb{E}_{\text{novel tasks}}[\text{Performance}] = \text{分布外泛化能力}}$$

**智能的本质不是已掌握的技能，而是获取新技能的效率。**

### Legg-Hutter 通用智能定义

$$\Gamma(\pi) = \sum_{\mu \in \mathcal{E}} 2^{-K(\mu)} \cdot V_\pi(\mu)$$

这个公式告诉我们：智能 = 在所有可能环境中的加权平均性能，权重由环境复杂度决定。

### 当前 AI 的位置

| 能力维度 | 状态 | 到 AGI 的差距 |
|----------|------|--------------|
| 知识覆盖 | ✅ 超越人类 | 已解决 |
| 语言处理 | ✅ 超越人类 | 已解决 |
| 流体推理 | ❌ 远低于人类 | **关键瓶颈** |
| 工作记忆 | ❌ 远低于人类 | **关键瓶颈** |
| 长期记忆 | ❌ 几乎为零 | **关键瓶颈** |

GPT-4/Claude 目前处于 **Level 2-3**（DeepMind 分类），距离真正的 AGI 还有约 **43%** 的差距。

---

## 三、创作方式的改变

这次经历让我意识到，公众号创作的方式已经发生了根本性的变化。

### 之前：我自己干写

```
传统流程：
选题 → 搜资料 → 写初稿 → 修改 → 排版 → 发布
(1h)   (3h)     (4h)     (2h)   (2h)   (10min)

⏱️ 总计：约 12+ 小时
😫 状态：独自承担所有环节
```

每一步都要自己来：选题要想、资料要找、文章要写、排版要调。最痛苦的是排版——为了一个字体、一个表格样式，要在公众号编辑器里反复调整。

### 现在：和 Claude Code 交互选择

```
AI 协作流程：
我提问 → Claude 搜集 → 我选选项 → Claude 生成 → 我审核 → Claude 发布
(1min)   (自动)        (点击)       (自动)       (5min)    (自动)

⏱️ 总计：约 2 小时
😊 状态：专注于创意和决策
```

**核心变化：从"输出者"变成了"决策者"。**

### 交互过程示例

**我说：**
```
人类如何实现 AGI 的指标？请将此问题转化为数学问题。
[search-mode]
```

**Claude Code 启动并行搜索后，给我选项：**
```
发现以下框架，请选择要深入了解的方向：

○ A. Legg-Hutter 通用智能定义（数学最严谨）
○ B. Chollet ARC-AGI 基准测试（实用性最强）
○ C. DeepMind 六级分类框架（业界最认可）
○ D. 全部整合，生成统一框架
```

**我选择 D，Claude Code 自动生成完整报告，然后又给我选项：**
```
是否发布到公众号？

○ 方案一：现代渐变风格
○ 方案二：Newsprint 学术风格（基于你的 Typora 主题）
○ 先预览效果
```

整个过程，我只需要做选择题和最后的审核。

---

## 四、公众号排版：遇到的坑

研究完成后，问题来了：如何把这份数学味十足的文章发布到公众号？

### 问题一：数学公式无法渲染

微信公众号不支持 LaTeX 公式。像这样的公式：

```
$$\Gamma(\pi) = \sum_{\mu \in \mathcal{E}} 2^{-K(\mu)} \cdot V_\pi(\mu)$$
```

在公众号里只能显示为乱码或纯文本。

### 问题二：表格样式丢失

Markdown 的表格在公众号里会失去边框、对齐等格式，看起来非常混乱。

### 问题三：字体限制

公众号不支持自定义字体。我想要的中文学术风格——楷体，根本无法通过公众号编辑器实现。

### 问题四：代码块不美观

技术文章中的代码片段，在公众号里缺乏语法高亮，难以阅读。

---

## 五、Claude Code 的解决方案

面对这些排版难题，我再次求助 Claude Code：「帮我生成一份适合公众号的 HTML，要美观，要有学术风格。」

Claude Code 给出了两个方案：

### 方案一：现代渐变风格

`publish-agi.ts` 采用了：
- 紫色渐变高亮框
- 内联 CSS 样式
- 现代化卡片设计
- 公众号兼容的 HTML 结构

```typescript
const styles = {
  highlightBox: `
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 12px;
  `,
  formula: `
    background: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
    font-family: "Courier New", monospace;
  `
};
```

### 方案二：Newsprint 学术风格（我的改写版本）

`publish-agi-newsprint.ts` 基于我喜欢的 Typora Newsprint 主题，通过 Claude Code 改写而成：

**原始来源**：Typora 的 Newsprint 主题是我日常写作最喜欢的风格——优雅的衬线字体、舒适的行距、学术感十足的排版。

**改写过程**：我告诉 Claude Code：「把 Typora Newsprint 主题改成公众号能用的内联 CSS 样式，保留楷体显示。」Claude Code 就帮我完成了从 CSS 到公众号 HTML 的转换。

```typescript
// Newsprint 主题核心样式（我从 Typora 改写的版本）
const style = {
  container: `
    font-family: "KaiTi", "楷体", "STKaiti", "华文楷体", Georgia, "Times New Roman";
    font-size: 16px;
    line-height: 1.75em;
    color: #1f0909;
  `,
  formula: `
    background-color: #f5f5f5;
    border-left: 4px solid #1f0909;
    padding: 1em;
    font-family: "Times New Roman", Times, serif;
  `
};
```

这个改写保留了 Newsprint 主题的精髓：
- 中文楷体优先，数字用衬线体
- 舒适的 1.75 倍行距
- 深褐色文字 `#1f0909`，比纯黑更柔和
- 公式块用左边框突出显示

### 关键技术点

1. **内联 CSS**：所有样式都写成 `style` 属性，避免公众号过滤外部样式

2. **字体回退链**：
   ```css
   font-family: "KaiTi", "楷体", "STKaiti", "华文楷体", Georgia, serif;
   ```
   虽然公众号无法强制加载楷体，但如果读者设备上有安装，就能显示。

3. **公式转换**：将 LaTeX 公式转换为 HTML 可渲染的形式：
   ```html
   <div style="${style.formula}">
     Γ(π) = Σ<sub>μ∈E</sub> 2<sup>-K(μ)</sup> · V<sub>π</sub>(μ)
   </div>
   ```

4. **表格样式**：手动为每个单元格添加样式，确保斑马纹效果：
   ```html
   <tr style="background-color: #e8e7e7;">
     <td>...</td>
   </tr>
   ```

---

## 六、最终效果

通过 Claude Code 自动生成的 CSS 方案，文章获得了：

- ✅ 优雅的学术风格排版
- ✅ 可读性强的数学公式展示
- ✅ 清晰的表格格式
- ✅ 公众号完美兼容

Claude Code 直接调用微信 API 创建了草稿，我只需要登录公众号后台审核发布即可。

---

## 七、思考：AI 辅助创作的边界

这次经历让我思考几个问题：

### 1. AI 能做什么？

- **资料搜集**：并行 Agent 大幅提升效率
- **内容生成**：结构化输出、数学形式化
- **问题解决**：排版难题、技术实现
- **API 调用**：直接与外部平台交互

### 2. 人类需要做什么？

- **提问**：定义问题的方向和深度
- **审核**：验证 AI 输出的准确性
- **决策**：选择风格、调整细节
- **发布**：最终的把关和分发

### 3. 效率提升

| 环节 | 传统方式 | AI 辅助 |
|------|---------|---------|
| 资料搜集 | 数天 | 数小时 |
| 内容整理 | 数小时 | 数分钟 |
| 排版调整 | 数小时 | 数分钟 |
| API 发布 | 手动复制粘贴 | 自动化 |

---

## 八、技术细节附录

### 使用的 Skills 清单

```
- search-mode: OpenCode 的并行搜索模式
- analyze-mode: 深度分析模式
- librarian agent: 学术文献检索
- oracle agent: 数学框架建议
- explore agent: 本地项目探索
- wechat-publisher: 微信公众号发布
```

### 相关文件

```
D:\Obsidian\AGI实现指标的数学形式化研究.md  # 原始研究文档
C:\Users\sksua\.claude\skills\wechat-publisher\publish-agi.ts  # 现代风格发布脚本
C:\Users\sksua\.claude\skills\wechat-publisher\publish-agi-newsprint.ts  # 学术风格发布脚本
```

### 关键命令

```bash
# 运行发布脚本
cd C:\Users\sksua\.claude\skills\wechat-publisher
node publish-agi-newsprint.ts
```

---

## 九、写在最后

这次「AGI 数学形式化研究」的创作过程，本身就是 AI 辅助内容生产的一个缩影：

1. **提问比回答更重要**：好的问题能引导 AI 进行深度探索
2. **工具链是关键**：Claude Code 的 Skills 系统让复杂任务变得简单
3. **人机协作是未来**：AI 处理繁琐事务，人类专注于创意和决策

当 AI 能帮我们解决「字体排版」这种琐碎问题时，我们才有更多精力去思考真正重要的事情——比如，AGI 到底意味着什么？

---

> **相关链接**
> - [Legg-Hutter 论文](https://arxiv.org/abs/0712.3329)
> - [Chollet 智力度量](https://arxiv.org/abs/1911.01547)
> - [DeepMind AGI 等级](https://arxiv.org/abs/2311.02462)
> - [ARC-AGI 基准测试](https://arcprize.org/arc-agi)

---

## 🎁 福利：本次任务用到的 Skills 分享

以下是本次创作过程中实际使用的 Skills，每个都可以直接安装使用。

### 1. 📰 News Aggregator Skill - 新闻聚合助手

**一句话介绍**：全网 28+ 信源一键聚合，自动生成精美早报。

**核心功能**：
- 覆盖 Hacker News、GitHub Trending、36Kr、华尔街见闻、Hugging Face Papers 等
- 内置 Deep Fetch 深度阅读，绕过 Cloudflare 抓取全文
- 多场景预设：综合早报、财经早报、科技早报、AI 深度日报
- 输出杂志级排版的 Markdown 报告

**安装方式**：
```bash
# 方法一：Openskills CLI（推荐）
openskills install git@github.com:cclank/news-aggregator-skill.git
openskills sync

# 方法二：NPX
npx skills add https://github.com/cclank/news-aggregator-skill

# 安装依赖
pip install -r requirements.txt
playwright install chromium
```

**使用示例**：
```
"news-aggregator-skill 如意如意"  # 唤醒交互菜单
"帮我跑一份财经早报"
"抓取 5 条最新的 GitHub 趋势，开启 Deep Fetch"
```

---

### 2. 📺 YouTube Summarizer - 视频字幕总结

**一句话介绍**：下载 YouTube 字幕，自动生成详细中文总结。

**核心功能**：
- 单视频字幕下载与总结
- 频道批量处理（最近 N 天视频）
- 支持多语言字幕
- 自动导出 Markdown 到指定路径

**安装方式**：
```bash
# 安装依赖
pip install youtube-transcript-api yt-dlp
```

**使用示例**：
```
"请总结这个视频：https://youtube.com/watch?v=xxx"
"获取 @ChannelName 最近30天的视频并总结"
```

---

### 3. 🚀 LoongFlow - 演化式 Agent 框架

**一句话介绍**：让 AI 通过 PES 范式自主优化代码，解决复杂问题。

**核心功能**：
- **PES 范式**：Plan → Execute → Summary，结构化思考
- **三种 Agent**：General（编程）、Math（算法优化）、ML（Kaggle 竞赛）
- **演化能力**：代码自动迭代优化，超越人类最佳

**实测成果**：
- 数学问题：11 项超越人类最佳，7 项超越 AlphaEvolve
- Kaggle：48 枚奖牌，其中 26 金

**安装方式**：
```bash
git clone https://github.com/your-repo/loongflow
cd loongflow
uv venv .venv --python 3.12
.\.venv\Scripts\activate
uv pip install -e .
```

**使用示例**：
```
"用 loongflow 优化这个算法"
"帮我跑一个数学优化任务"
```

---

### 4. 📋 AI Task Planner - AI 优先任务规划

**一句话介绍**：把复杂项目拆解成微任务，标记哪些 AI 可以帮忙。

**核心功能**：
- 项目分解：阶段 → 步骤 → 微任务
- 执行标记：🤖 AI / 👤 人工 / 🤝 协作
- 工具推荐：为每类任务匹配最佳 AI 工具
- 减少决策疲劳

**核心理念**：
> 磨斧头——前期花几分钟规划，后期节省数小时。

**使用示例**：
```
"帮我规划一个产品 PRD 撰写项目"
"这个周报项目，帮我做 AI 任务规划"
```

---

### 5. 📤 WeChat Publisher - 公众号发布助手

**一句话介绍**：Markdown 转 HTML，一键发布到公众号。

**核心功能**：
- Markdown 转 微信公众号兼容 HTML
- 内置 Newsprint 学术风格样式
- 自动获取 Access Token
- 创建草稿到公众号后台

**关键技术点**：
- 内联 CSS，避免公众号过滤
- 字体回退链：楷体 → Georgia → Times New Roman
- LaTeX 公式转 HTML 可渲染形式

**使用示例**：
```bash
cd ~/.claude/skills/wechat-publisher
npx tsx publish-agi-newsprint.ts
```

---

### 安装汇总

| Skill | 安装命令 | 来源 |
|-------|----------|------|
| News Aggregator | `openskills install cclank/news-aggregator-skill` | GitHub |
| YouTube Summarizer | `pip install youtube-transcript-api yt-dlp` | PyPI |
| LoongFlow | `git clone && uv pip install -e .` | 本地项目 |
| AI Task Planner | 内置 | Claude Code 内置 |
| WeChat Publisher | 内置 | 本地 skill |

---

> **提示**：这些 Skills 都可以在 Claude Code 中直接使用，只需通过自然语言触发即可。

---

## 🔮 可以改进的地方

这个工作流已经大幅提升了我的创作效率，但还有很多可以优化的空间：

### 1. 排版样式更加丰富

目前只有两种预设风格，未来可以支持：
- 🎨 更多 Typora 主题（GitHub、Academic、Vue 等）
- 🌙 暗黑模式支持
- 📱 移动端适配优化
- 🖼️ 图片自动压缩和 CDN 上传

### 2. 智能化程度更高

- 🤖 自动识别文章类型（技术/财经/生活），推荐最佳排版风格
- 📊 数据可视化：自动生成图表并嵌入
- 🔗 引用自动补全：DOI 链接自动转换为格式化引用
- ✍️ 风格模仿：学习你的历史文章风格

### 3. 多平台同步

目前只支持微信公众号，可以扩展到：
- 📕 小红书（图文+短视频脚本）
- 🎵 抖音/B站（视频脚本+字幕）
- 🐦 Twitter/X（自动裁剪成推文串）
- 📰 知乎/专栏（保留完整 LaTeX 公式）

### 4. 协作功能

- 👥 多人审阅流程
- 💬 评论批注（类似 Google Docs）
- 📝 版本历史和回滚

---

## 🙌 一起来玩！

这个工作流的所有 Skills，我都会逐步整理开源到我的 GitHub：

> **GitHub: https://github.com/kevinsong0/claude-code-skills**

欢迎：
- ⭐ Star 支持
- 🍴 Fork 后自定义你的版本
- 🐛 提 Issue 反馈问题
- 🔀 发 PR 贡献新功能

### 我特别期待看到

1. **你用这个工作流创作的文章** — 评论区分享链接
2. **你自定义的排版风格** — 新闻、财经、技术、生活不同模板
3. **你扩展的新平台** — 小红书、知乎、B站...
4. **你发现的新玩法** — AI 辅助创作还有什么可能？

---

> **如果这篇文章对你有帮助，点个「在看」，让更多人发现 AI 辅助创作的可能性。**

---

#ClaudeCode  #AI写作 #公众号排版 #AGI #人工智能 #开源