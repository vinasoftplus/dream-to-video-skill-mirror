# Dream-to-Video Skill

将梦境文字自动转化为电影级视频的 AI agent 技能。描述梦境后，agent 会为[即梦](https://jimeng.jianying.com)浏览器流程或 Gemini Developer API 中的 Google Veo 生成专业提示词。即梦支持队列生成和后处理；Veo 支持同步单次生成视频。

## 工作原理

```
梦境文字 → AI 转化为电影级提示词 → 即梦队列/浏览器或 Veo API → 下载 → 视频文件
```

1. **提示词转化** — AI agent 按照 10 条严格规则（照片级写实、鱼眼镜头、无文字叠加、非言语叙事等）将梦境描述转化为详细的电影级视频提示词
2. **队列提交** — 提示词被加入本地任务队列（SQLite + JSONL）
3. **视频生成** — 即梦任务通过后台 Playwright Worker 执行；Veo 任务通过 Gemini Developer API 提交并轮询长时间运行的生成任务
4. **下载与后处理** — Veo 视频直接下载到输出目录。即梦视频会下载并叠加「椭圆破碎」边缘特效，同时输出原版和特效版

## 安装

### 通过 skills CLI

```bash
npx skills add vinasoftplus/dream-to-video-skill-mirror -s dream-to-video
```

### 手动安装

克隆仓库并将 skill 目录软链接到你的 agent 技能目录：

```bash
git clone https://github.com/vinasoftplus/dream-to-video-skill-mirror.git
mkdir -p ~/.claude/skills
ln -s "$(pwd)/dream-to-video-skill-mirror/skills/dream-to-video" ~/.claude/skills/dream-to-video
```

## 环境要求

- Python >= 3.10
- Chromium（通过 Playwright 安装）
- 以下任一 API 提供商的 Key：

| 提供商 | 模型 | 获取 Key |
|--------|------|----------|
| **Claude**（默认） | claude-sonnet-4 | [console.anthropic.com](https://console.anthropic.com/settings/keys) |
| **OpenAI** | gpt-4o | [platform.openai.com](https://platform.openai.com/api-keys) |
| **OpenRouter** | 任意模型 | [openrouter.ai](https://openrouter.ai/keys) |
| **Google Gemini** | gemini-2.5-flash | [aistudio.google.com](https://aistudio.google.com/apikey) |

Veo 使用 Gemini Developer API 生成视频，并复用 `GEMINI_API_KEY`。默认模型为 `veo-3.1-generate-preview`，生成默认时长为 8 秒并包含音频。

## 配置

安装技能后，克隆本仓库以获取 Python 工具链：

```bash
git clone https://github.com/vinasoftplus/dream-to-video-skill-mirror.git
cd dream-to-video-skill-mirror/dream_to_video
cp .env.example .env
# 运行前在 .env 中填写所需的 API Key
pip install -r requirements.txt
playwright install chromium
```

然后登录即梦平台（仅需一次二维码扫码）：

```bash
python main.py login
```

## 使用

配置完成后，直接向 AI agent 描述你的梦境即可：

> "我梦到自己赤脚在海滨步道上奔跑，周围全是密密麻麻的海狮..."

Agent 会自动：
1. 将文字转化为电影级视频提示词
2. 提交到任务队列（`python main.py add "<提示词>"`）
3. 启动后台 Worker（`python main.py worker`）
4. 视频生成完毕后通知你，文件保存在 `dream_to_video/output/`

### CLI 命令

| 命令 | 说明 |
|------|------|
| `python main.py login` | 扫码登录即梦平台 |
| `python main.py verify` | 检查登录状态 |
| `python main.py add "<提示词>"` | 添加提示词到任务队列 |
| `python main.py worker` | 启动后台 Worker |
| `python main.py status` | 查看任务进度 |
| `python main.py generate "<提示词>"` | 单次同步生成 |
| `python main.py serve` | 启动 FastAPI Web 服务 |

若要使用 Veo 单次生成视频（而不是即梦），运行：

```bash
python main.py generate --provider veo "电影感视频提示词"
```

请先在 `dream_to_video/.env` 中设置 `GEMINI_API_KEY`。Veo 命令会等待任务完成，并将单个 MP4 保存到 `dream_to_video/output/`。批量 `worker` 命令目前仍面向即梦。

### 输出

每个任务在 `dream_to_video/output/` 下生成两个视频文件：

- `task_XXX_YYYYMMDD_HHMMSS.mp4` — 原版视频
- `task_XXX_YYYYMMDD_HHMMSS_elliptic-shatter.mp4` — 椭圆破碎边缘特效版

## 自定义工作流

本仓库可作为你自己视频生成工作流的起点。当前支持即梦浏览器自动化和 Google Veo 单次同步生成。修改位置与建议步骤请见[自定义指南](./CUSTOMIZING.md)。提示词规则分别写在 `skills/dream-to-video/SKILL.md` 和 `dream_to_video/prompt_engine.py`，修改时请保持两处一致。

## 许可证

[MIT](./LICENSE)
