# WeChat Publisher Skill

微信公众号文章发布工具，将 Markdown 文档转换为微信公众号兼容的 HTML 格式并发布。

## 功能

- Markdown 转 HTML（微信公众号兼容格式）
- 自动获取 Access Token
- 创建草稿并上传封面图片
- 支持自定义样式（字体、颜色、排版）
- **🆕 社区互动模块**：自动生成改进建议 + Skills 福利分享 + 号召参与

## 文件说明

| 文件 | 用途 |
|------|------|
| `wechat-api.ts` | 微信公众号 API 封装 |
| `publish-v2.ts` | 当前版本的发布脚本 |
| `publish-agi.ts` | AGI 文章专用发布脚本 |
| `publish-agi-newsprint.ts` | Newsprint 主题样式发布脚本 |
| `test-preview.html` | 本地预览测试文件 |
| `templates/community-engagement.ts` | 🆕 社区互动模块（改进建议 + 福利 + 号召） |

## 使用方法

```bash
cd C:/Users/sksua/.claude/skills/wechat-publisher
npx tsx publish-v2.ts
```

## ⚠️ 开发规范（必须遵守）

### 1. 测试优先原则

**任何开发类任务，必须先进行测试验证，再提交结果。**

适用场景：
- 修改发布脚本逻辑
- 调整 HTML 样式
- 新增功能
- 修复 Bug

### 2. 测试流程

```
1. 本地预览测试
   ├── 生成 test-preview.html
   └── 在浏览器中打开验证样式

2. 草稿测试
   ├── 运行脚本创建草稿
   └── 登录 mp.weixin.qq.com 预览效果

3. 用户确认
   ├── 等待用户反馈
   └── 确认无误后才算完成
```

### 3. 样式测试清单

发布前必须验证：
- [ ] 中文字体：楷体（KaiTi）
- [ ] 英文字体：Times New Roman
- [ ] 数字字体：Times New Roman
- [ ] 公式显示正确
- [ ] 列表项正确换行（不合并显示）
- [ ] 表格对齐正常
- [ ] 代码块样式正确

### 4. 微信公众号兼容性限制

| 不支持 | 替代方案 |
|--------|----------|
| `<ul>`, `<ol>`, `<li>` | `<p style="padding-left: 20px;">• item</p>` |
| `<code>` 块 | `<span style="background: #e8e8e8; padding: 2px 6px;">` |
| 外部 CSS | 内联 `style=""` 属性 |
| `<script>` | 完全禁止 |
| 部分字体 | 使用微信内置字体 |

## 微信公众号配置

- 公众号：****
- AppID: `****`
- AppSecret: 已配置

## 常见问题

### Q: 列表项被合并成一行？
A: 微信公众号不支持列表标签，需使用 `<p style="padding-left: 20px;">• item</p>` 替代。

### Q: 英文字体不是 Times New Roman？
A: 检查 font-family 顺序，确保 Times New Roman 在 Georgia 之前：
```css
font-family: KaiTi, 楷体, STKaiti, 华文楷体, Times New Roman, Times, serif;
```

### Q: 如何预览效果？
A: 生成 test-preview.html 后在浏览器打开，或创建草稿后在公众号后台预览。

---

## 🆕 社区互动模块

每次发布文章时，可以在末尾自动添加「改进建议 + Skills 福利 + 号召参与」，提升社区互动。

### 使用方式

```typescript
import { generateCommunitySection, defaultSkillsConfig } from './templates/community-engagement';

// 在文章内容末尾添加
const fullContent = articleContent + generateCommunitySection({
  githubUrl: 'https://github.com/sksua/claude-code-skills',
  skillsUsed: [
    { name: '📰 News Aggregator', desc: '28+ 信源聚合', installCmd: 'openskills install' },
    { name: '🚀 LoongFlow', desc: 'AI 自主优化代码', installCmd: 'git clone' }
  ]
});
```

### 配置选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `githubUrl` | GitHub 仓库链接 | `https://github.com/kevinsong0/claude-code-skills` |
| `projectName` | 项目名称 | `Claude Code Skills` |
| `skillsUsed` | 本次用到的 Skills 列表 | `[]` |
| `customImprovements` | 自定义改进建议 | `[]` |
| `showBonus` | 是否显示福利部分 | `true` |

### 生成内容

1. **🎁 福利：本次用到的 Skills** — 表格展示，带安装命令
2. **🔮 可以改进的地方** — 排版、智能化、多平台、协作
3. **🙌 一起来玩** — GitHub 链接、号召参与

### 效果

```
当人气够旺时，可以：
- 专门做一期视频/文章讨论改进建议
- 收集社区贡献的新功能
- 形成良性循环，吸引更多人参与
```
