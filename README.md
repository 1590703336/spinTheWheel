## Double Spin Wheel

课堂小游戏 “Double Spin Wheel + Flying Chess” 同时支持：

1. 桌面版 `spinTheWheel.py`（Tkinter GUI）
2. Web 版（React + FastAPI + OpenRouter），可一键部署到 Vercel

所有题库、得分与特殊格逻辑保持一致。感谢 Liz 提供题库。

---

## 目录结构

```
.
├── spinTheWheel.py        # 现有 Tkinter 游戏
├── backend/               # Web 端共享的题库 & 业务逻辑
├── api/                   # FastAPI Serverless functions（Vercel）
├── frontend/              # React + Vite 前端
├── requirements.txt       # Python 依赖（API）
├── env.example            # 复制为 .env，填写 OpenRouter 信息
└── vercel.json            # Vercel 构建与函数配置
```

---

## 环境变量

将 `env.example` 复制为 `.env` 并填写：

```
OPENROUTER_API_KEY=your-key
YOUR_SITE_URL=https://your-site-url.com
YOUR_APP_NAME=Double Spin Wheel Game
```

部署到 Vercel 时，在 “Settings → Environment Variables” 中填入相同字段。

---

## 本地开发

### 后端（API）

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn api.index:app --reload --port 8000
```

### 前端（React + Vite）

需要 Node.js ≥ 18：

```bash
cd frontend
npm install
npm run dev
```

Vite dev server（默认 5173）已在 `vite.config.ts` 中代理 `/api` → `http://127.0.0.1:8000`，因此前端可直接请求本地 FastAPI。

---

## Vercel 部署

1. 将仓库推送到 GitHub 并在 Vercel 选择 “Import Project”
2. 在 `Settings → Environment Variables` 中配置：
   - `OPENROUTER_API_KEY`
   - `YOUR_SITE_URL`
   - `YOUR_APP_NAME`
3. 直接部署：`vercel.json` 会
   - 运行 `cd frontend && npm install && npm run build`
   - 将静态文件输出 `frontend/dist`
   - 自动启用 `api/*.py` 为 Python Serverless Functions

部署完成后，访问根域名即可使用 Web 版本，`/api/*` 则提供 REST 接口供其他客户端使用。

