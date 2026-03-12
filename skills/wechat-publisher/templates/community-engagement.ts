/**
 * 社区互动模块 - 自动生成文章末尾的改进建议和号召参与内容
 *
 * 使用方式：
 * 1. 在发布脚本中 import { generateCommunitySection } from './templates/community-engagement'
 * 2. 在文章末尾调用 generateCommunitySection(config)
 */

interface CommunityConfig {
  /** GitHub 仓库链接 */
  githubUrl?: string;
  /** 项目名称 */
  projectName?: string;
  /** 本次用到的 skills 列表 */
  skillsUsed?: Array<{
    name: string;
    desc: string;
    installCmd?: string;
  }>;
  /** 自定义改进建议 */
  customImprovements?: string[];
  /** 是否显示"福利"部分 */
  showBonus?: boolean;
}

const defaultConfig: CommunityConfig = {
  githubUrl: 'https://github.com/kevinsong0/claude-code-skills',
  projectName: 'Claude Code Skills',
  showBonus: true
};

/**
 * 生成"可以改进的地方"部分
 */
function generateImprovements(customItems?: string[]): string {
  const defaultImprovements = [
    {
      category: '🎨 排版样式更丰富',
      items: ['更多 Typora 主题支持', '暗黑模式', '移动端适配', '图片自动压缩']
    },
    {
      category: '🤖 智能化程度更高',
      items: ['自动识别文章类型', '数据可视化', '风格模仿学习']
    },
    {
      category: '📱 多平台同步',
      items: ['小红书图文', '抖音/B站脚本', 'Twitter 推文串', '知乎专栏']
    },
    {
      category: '👥 协作功能',
      items: ['多人审阅', '评论批注', '版本历史']
    }
  ];

  let html = `
<p style="font-size: 18px; font-weight: bold; margin: 30px 0 15px; padding-left: 12px; border-left: 4px solid #667eea;">🔮 可以改进的地方</p>
<p style="margin: 10px 0; color: #666;">这个工作流已经大幅提升了我的创作效率，但还有很多可以优化的空间：</p>
`;

  defaultImprovements.forEach(imp => {
    html += `
<p style="margin: 15px 0 8px; font-weight: bold;">${imp.category}</p>
<p style="margin: 5px 0; padding-left: 20px; color: #555;">• ${imp.items.join('</p><p style="margin: 5px 0; padding-left: 20px; color: #555;">• ')}</p>
`;
  });

  if (customItems && customItems.length > 0) {
    html += `<p style="margin: 15px 0 8px; font-weight: bold;">💡 其他建议</p>`;
    customItems.forEach(item => {
      html += `<p style="margin: 5px 0; padding-left: 20px; color: #555;">• ${item}</p>`;
    });
  }

  return html;
}

/**
 * 生成"福利：Skills 分享"部分
 */
function generateBonusSection(skills: CommunityConfig['skillsUsed']): string {
  if (!skills || skills.length === 0) return '';

  let html = `
<hr style="border: none; border-top: 1px solid #c5c5c5; margin: 25px 0;">
<p style="font-size: 18px; font-weight: bold; margin: 25px 0 15px; padding-left: 12px; border-left: 4px solid #667eea;">🎁 福利：本次用到的 Skills</p>
<p style="margin: 10px 0; color: #666;">以下 Skills 可以直接安装使用：</p>

<table style="width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 14px;">
<tr style="background: #667eea; color: white;"><th style="padding: 10px; text-align: left;">Skill</th><th style="padding: 10px; text-align: left;">介绍</th><th style="padding: 10px; text-align: left;">安装</th></tr>
`;

  skills.forEach((skill, index) => {
    const bg = index % 2 === 0 ? '' : 'background: #f8f8f8;';
    html += `<tr style="${bg}"><td style="padding: 10px; border-bottom: 1px solid #eee;">${skill.name}</td><td style="padding: 10px; border-bottom: 1px solid #eee;">${skill.desc}</td><td style="padding: 10px; border-bottom: 1px solid #eee; font-family: Courier New, monospace; font-size: 12px;">${skill.installCmd || '内置'}</td></tr>`;
  });

  html += `</table>`;
  return html;
}

/**
 * 生成"一起来玩"号召部分
 */
function generateCallToAction(githubUrl: string, projectName: string): string {
  return `
<hr style="border: none; border-top: 1px solid #c5c5c5; margin: 25px 0;">
<p style="font-size: 18px; font-weight: bold; margin: 25px 0 15px; padding-left: 12px; border-left: 4px solid #667eea;">🙌 一起来玩！</p>

<p style="margin: 10px 0;">所有 Skills 都会逐步整理开源到 GitHub：</p>

<p style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; margin: 15px 0; border-radius: 8px; text-align: center; font-size: 16px;">
<strong>GitHub: ${githubUrl}</strong>
</p>

<p style="margin: 10px 0;">欢迎：</p>
<p style="margin: 5px 0; padding-left: 20px;">⭐ Star 支持</p>
<p style="margin: 5px 0; padding-left: 20px;">🍴 Fork 后自定义你的版本</p>
<p style="margin: 5px 0; padding-left: 20px;">🐛 提 Issue 反馈问题</p>
<p style="margin: 5px 0; padding-left: 20px;">🔀 发 PR 贡献新功能</p>

<p style="margin: 20px 0 10px; font-weight: bold;">我特别期待看到：</p>
<p style="margin: 5px 0; padding-left: 20px;">1. 你用这个工作流创作的文章</p>
<p style="margin: 5px 0; padding-left: 20px;">2. 你自定义的排版风格</p>
<p style="margin: 5px 0; padding-left: 20px;">3. 你扩展的新平台</p>
<p style="margin: 5px 0; padding-left: 20px;">4. 你发现的新玩法</p>

<hr style="border: none; border-top: 1px solid #c5c5c5; margin: 25px 0;">

<p style="background: #f0f7ff; padding: 15px; margin: 15px 0; border-radius: 8px; text-align: center; color: #666;">
💡 <strong>如果这篇文章对你有帮助，点个「在看」，让更多人发现 AI 辅助创作的可能性。</strong>
</p>
`;
}

/**
 * 主函数：生成完整的社区互动部分
 */
export function generateCommunitySection(config: CommunityConfig = {}): string {
  const finalConfig = { ...defaultConfig, ...config };

  let html = '<hr style="border: none; border-top: 1px solid #c5c5c5; margin: 30px 0;">';

  // 福利部分
  if (finalConfig.showBonus && finalConfig.skillsUsed) {
    html += generateBonusSection(finalConfig.skillsUsed);
  }

  // 改进建议
  html += generateImprovements(finalConfig.customImprovements);

  // 号召参与
  html += generateCallToAction(finalConfig.githubUrl!, finalConfig.projectName!);

  return html;
}

// 使用示例
const exampleSkills = [
  { name: '📰 News Aggregator', desc: '28+ 信源一键聚合', installCmd: 'openskills install news-aggregator' },
  { name: '📺 YouTube Summarizer', desc: '视频字幕下载+总结', installCmd: 'pip install youtube-transcript-api' },
  { name: '🚀 LoongFlow', desc: 'AI 自主优化代码', installCmd: 'git clone loongflow' },
  { name: '📤 WeChat Publisher', desc: 'Markdown 转公众号 HTML', installCmd: '内置' }
];

// 导出示例配置
export const defaultSkillsConfig = exampleSkills;