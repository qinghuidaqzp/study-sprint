# Study Sprint MVP

一个面向学生、补考复习、培训场景的学习资料整理与复习生成器。上传录音、PPT、PDF、讲义后，系统会把材料统一解析为结构化片段，并生成：

- 复习提纲
- 章节总结
- 高频考点
- 练习题
- 速记卡片

这个项目聚焦“学习提效”和“考试复习”，不是会议纪要或办公协作工具。

## 技术栈

- 前端：Next.js App Router + TypeScript
- 后端：FastAPI + SQLAlchemy
- 文件解析：PyMuPDF、python-pptx、Whisper 兼容方案
- 数据库：PostgreSQL
- 文件存储：本地存储，预留未来切换对象存储的空间
- AI 调用：独立 AI Provider 抽象，支持 `mock` 和 OpenAI 兼容接口

## 目录结构

```text
appthird/
  backend/
    app/
      api/
      core/
      db/
      models/
      schemas/
      services/
      utils/
      main.py
    storage/
      uploads/
      exports/
    .env.example
    requirements.txt
    requirements-audio.txt
  frontend/
    app/
    components/
    lib/
    .env.example
    package.json
  .env.example
  docker-compose.yml
  package.json
  requirements.txt
  README.md
```

## MVP 已实现内容

### 1. 文件上传

支持上传：

- `mp3`
- `wav`
- `m4a`
- `pptx`
- `pdf`
- `txt`
- `md`

后端统一走 `/api/tasks` 上传接口，并做基础格式校验与大小限制。

### 2. 内容解析

- 音频：使用 Whisper 兼容方案转写
- PPT：按页提取文字
- PDF：按页提取正文
- 文本/Markdown：直接读取并分段

系统会把不同来源统一整理为带来源标签的文本片段，例如：

- `PDF 第 3 页`
- `PPT 第 8 页`
- `音频 15s - 42s`
- `文本 第 2 段`

### 3. 学习资料生成

后端会生成五类内容：

- `outline` 复习提纲
- `chapter_summary` 章节总结
- `key_points` 高频考点
- `quiz` 练习题
- `flashcards` 速记卡片

生成逻辑通过统一模板管理，避免提示词散落在业务代码中。

### 4. 页面

- `/` 上传页
- `/tasks/[id]` 结果页
- `/history` 历史记录页

### 5. 导出

- Markdown 导出
- PDF 导出

## 环境要求

推荐：

- Node.js 18+
- Python 3.11+
- PostgreSQL 14+

说明：基础后端依赖默认不强制安装 `faster-whisper`，这样在 Python 3.13 环境下也能先跑通 PDF / PPT / 文本主流程；如果需要本地音频转写，再额外安装音频依赖。

## 安装步骤

### 1. 启动 PostgreSQL

项目提供了本地开发用数据库：

```bash
docker compose up -d
```

数据库默认配置：

- Host: `localhost`
- Port: `5432`
- DB: `study_sprint`
- User: `postgres`
- Password: `postgres`

如果当前机器没有 PostgreSQL，也可以先用 SQLite 快速验证主流程：`DATABASE_URL=sqlite:///E:/Dasan/appthird/backend/study_sprint.db`。

### 2. 安装后端依赖

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

或者只装后端基础依赖：

```bash
pip install -r backend/requirements.txt
```

如果你需要本地音频转写，再额外安装：

```bash
pip install -r backend/requirements-audio.txt
```

### 3. 配置环境变量

后端：

```bash
copy backend\.env.example backend\.env
```

前端：

```bash
copy frontend\.env.example frontend\.env.local
```

默认 `mock` 模式下，不需要 AI Key 也能跑完整流程；只是生成质量会低于真实大模型。

如果你想接入真实模型：

- 设置 `AI_PROVIDER` 为非 `mock`
- 配置 `AI_API_KEY`
- 配置 `AI_BASE_URL`
- 配置 `AI_MODEL`

如果你想把音频转写走 OpenAI 兼容接口：

- 设置 `WHISPER_BACKEND=openai`
- 保持 `AI_API_KEY` 可用

### 4. 启动后端

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### 5. 安装并启动前端

```bash
cd frontend
npm install
npm run dev
```

前端默认运行在：

- `http://localhost:3000`

后端默认运行在：

- `http://localhost:8000`

## 环境变量说明

### 后端

- `APP_NAME`：应用名
- `APP_ENV`：运行环境
- `DATABASE_URL`：默认使用 PostgreSQL，也可临时改成 `sqlite:///E:/Dasan/appthird/backend/study_sprint.db` 做本地验证
- `CORS_ORIGINS`：允许的前端域名列表
- `MAX_UPLOAD_SIZE_MB`：上传大小限制
- `AI_PROVIDER`：`mock` 或 OpenAI 兼容 provider
- `AI_BASE_URL`：模型服务地址
- `AI_API_KEY`：模型服务密钥
- `AI_MODEL`：聊天模型名称
- `WHISPER_BACKEND`：`local` 或 `openai`，其中 `local` 需要额外安装 `backend/requirements-audio.txt`
- `WHISPER_MODEL_SIZE`：本地 Whisper 模型规格

### 前端

- `NEXT_PUBLIC_API_BASE_URL`：后端 API 基地址

## API 简述

- `GET /api/health`：健康检查
- `POST /api/tasks`：创建任务并上传文件
- `POST /api/tasks/{task_id}/process`：重新处理任务
- `GET /api/tasks`：历史记录列表
- `GET /api/tasks/{task_id}`：任务详情
- `GET /api/tasks/{task_id}/segments`：全部解析片段
- `GET /api/tasks/{task_id}/export/markdown`：导出 Markdown
- `GET /api/tasks/{task_id}/export/pdf`：导出 PDF

## 运行流程

1. 前端上传资料并创建任务
2. FastAPI 保存文件与任务记录
3. 后端解析文件，抽取结构化文本片段
4. AI Provider 基于模板生成五类复习内容
5. 前端轮询任务状态并展示结果
6. 用户可导出 Markdown / PDF

## 关键设计说明

### 1. AI Provider 可替换

`backend/app/services/ai/` 下已拆分为：

- `mock_provider.py`
- `openai_provider.py`
- `factory.py`
- `prompt_templates.py`

后续如果切到别的模型服务，只需新增 Provider 实现并在工厂中切换。

### 2. 文件存储可替换

当前使用本地存储：

- 上传目录：`backend/storage/uploads/`
- 导出目录：`backend/storage/exports/`

未来可把 `services/storage/` 替换为 S3、OSS、MinIO 等对象存储。

### 3. 任务处理保持轻量

MVP 阶段没有引入 Celery、Redis、消息队列，而是采用 FastAPI BackgroundTasks + 前端轮询的简单方案。

### 4. 生成逻辑偏考试复习

提示词模板明确要求：

- 层次分明
- 保留原始知识点
- 强调定义、公式、结论、流程
- 避免空话
- 题目贴近材料
- 信息不足时标记“基于现有材料推测”

## 后续可扩展点

- 接入更强的模型服务，提升题目与卡片质量
- 对大文件增加异步任务队列
- 增加按课程/章节筛选结果
- 支持 DOCX、图片 OCR
- 支持结果编辑和二次导出
- 支持 S3/OSS 文件存储
- 增加用户系统与多任务隔离
- 增加更细粒度的题型，如判断题、填空题、案例题

## 当前已知限制

- `mock` 模式主要用于保证本地流程可跑通，生成质量不代表最终上限
- 音频本地转写依赖额外安装的 `faster-whisper`，第一次运行可能较慢
- PDF 导出采用 MVP 简化方案，版式偏实用，不追求复杂排版
- 当前历史记录为单用户本地开发模式，没有登录系统

## 快速验收建议

你可以按下面顺序测试：

1. 上传一个 `txt` 或 `md` 文件，确认主流程可跑通
2. 上传一个 `pdf`，检查页码片段是否正确
3. 上传一个 `pptx`，检查按页提取是否正常
4. 如已配置 Whisper，再测试音频转写
5. 在结果页检查 5 个模块是否都有输出
6. 下载 Markdown / PDF，确认可打开