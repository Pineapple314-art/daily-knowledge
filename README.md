# 每日杂学 · 随机知识推荐

每日推荐各领域知识，随机展示冷热杂学，内置 AI 知识助手引导批判性思考。

## 功能

- **随机推荐**：每日随机推荐知识，无偏好算法，无信息茧房
- **多领域覆盖**：90+ 条知识，涵盖物理、生物、心理、历史、医学等
- **冷热知识**：标注冷知识（少见但有趣）和热知识（常见但重要）
- **来源可靠**：每条知识附有学术期刊或权威媒体来源链接
- **AI 知识助手**：内置免费 AI，可对知识提问，引导批判性思维
- **本地存储**：记录已读知识，避免重复推荐

## 本地运行

```bash
python server.py
```

打开浏览器访问 http://localhost:8090

## 部署到 Vercel

### 方式一：命令行部署

```bash
# 安装 Vercel CLI
npm i -g vercel

# 在项目根目录执行
vercel

# 按提示操作即可，部署完成后会获得一个公开 URL
```

### 方式二：GitHub 关联部署

1. 将此仓库推送到 GitHub
2. 登录 [vercel.com](https://vercel.com)，点击 "New Project"
3. 选择 GitHub 仓库，Vercel 会自动检测配置
4. 点击 "Deploy"，等待构建完成
5. 获得公开访问地址

## 项目结构

```
├── index.html       # 主页面（UI + 交互逻辑）
├── knowledge.js     # 知识库（90+ 条知识数据）
├── server.py        # 本地开发服务器（静态文件 + AI 代理）
├── api/
│   └── ask.py       # Vercel serverless 函数（AI 代理）
├── vercel.json      # Vercel 部署配置
└── .gitignore
```

## 技术栈

- 纯 HTML/CSS/JavaScript（无框架）
- Python（Vercel serverless 函数）
- Pollinations AI（免费 AI 接口，无需 API Key）
- localStorage（本地状态存储）
