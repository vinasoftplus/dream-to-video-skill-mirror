# Dream-to-Video Skill

[中文文档](./README.zh-CN.md)

AI agent skill that transforms dream text into cinematic videos. Describe your dream, and the agent generates a professional prompt for either the [Jimeng](https://jimeng.jianying.com) browser workflow or Google Veo through the Gemini Developer API. Jimeng supports queued generation and post-processing; Veo is available for synchronous single-video generation.

## How It Works

```
Dream text → AI transforms to cinematic prompt → Jimeng queue/browser or Veo API → Download → Video files
```

1. **Prompt transformation** — The AI agent converts your dream description into a detailed cinematic video prompt following 10 strict rules (photorealistic style, fisheye lens, no text overlays, silent narrative, etc.)
2. **Queue submission** — The prompt is added to a local task queue (SQLite + JSONL)
3. **Video generation** — Jimeng tasks use a background Playwright worker; Veo tasks use the Gemini Developer API and poll the long-running generation operation
4. **Download & post-processing** — Veo videos download directly to the output folder. Jimeng videos are downloaded and automatically processed with an "Elliptic Shatter" edge effect, outputting both the original and effect versions

## Install

### Via skills CLI

```bash
npx skills add vinasoftplus/dream-to-video-skill-mirror -s dream-to-video
```

### Manual install

Clone the repo and symlink the skill directory into your agent's skill folder:

```bash
git clone https://github.com/vinasoftplus/dream-to-video-skill-mirror.git
mkdir -p ~/.claude/skills
ln -s "$(pwd)/dream-to-video-skill-mirror/skills/dream-to-video" ~/.claude/skills/dream-to-video
```

## Requirements

- Python >= 3.10
- Chromium (installed via Playwright)
- An API key from any supported provider:

| Provider | Model | Get a key |
|----------|-------|-----------|
| **Claude** (default) | claude-sonnet-4 | [console.anthropic.com](https://console.anthropic.com/settings/keys) |
| **OpenAI** | gpt-4o | [platform.openai.com](https://platform.openai.com/api-keys) |
| **OpenRouter** | any model | [openrouter.ai](https://openrouter.ai/keys) |
| **Google Gemini** | gemini-2.5-flash | [aistudio.google.com](https://aistudio.google.com/apikey) |

Veo generation uses the Gemini Developer API and the same `GEMINI_API_KEY`. The default Veo model is `veo-3.1-generate-preview`, which produces an 8-second video with audio.

## Setup

After installing the skill, clone this repo to get the Python toolchain:

```bash
git clone https://github.com/vinasoftplus/dream-to-video-skill-mirror.git
cd dream-to-video-skill-mirror/dream_to_video
cp .env.example .env
# Add your API key(s) to .env before running the tools
pip install -r requirements.txt
playwright install chromium
```

Then log in to the Jimeng platform (one-time QR code scan):

```bash
python main.py login
```

## Usage

Once set up, just describe a dream to your AI agent:

> "I dreamed I was running barefoot on a coastal boardwalk surrounded by hundreds of sea lions..."

The agent will:
1. Transform your text into a cinematic video prompt
2. Submit it to the queue (`python main.py add "<prompt>"`)
3. Start the background worker (`python main.py worker`)
4. Notify you when the video is ready in `dream_to_video/output/`

### CLI Commands

| Command | Description |
|---------|-------------|
| `python main.py login` | Log in to Jimeng via QR code |
| `python main.py verify` | Check login status |
| `python main.py add "<prompt>"` | Add a prompt to the task queue |
| `python main.py worker` | Start background worker |
| `python main.py status` | View task progress |
| `python main.py generate "<prompt>"` | Single synchronous generation |
| `python main.py serve` | Start FastAPI web server |

To generate a single video with Veo instead of Jimeng, run:

```bash
python main.py generate --provider veo "A cinematic video prompt"
```

Set `GEMINI_API_KEY` in `dream_to_video/.env` first. Veo generation runs synchronously and saves one MP4 in `dream_to_video/output/`. The batch `worker` command remains Jimeng-specific.

### Output

Each task produces two video files in `dream_to_video/output/`:

- `task_XXX_YYYYMMDD_HHMMSS.mp4` — Original video
- `task_XXX_YYYYMMDD_HHMMSS_elliptic-shatter.mp4` — With shattered-glass edge effect

## Customize Your Workflow

This repository is a starting point for building your own video-generation workflow. It currently supports Jimeng browser automation and synchronous single-video generation through Google Veo. Start with [CUSTOMIZING.md](./CUSTOMIZING.md) for a map of the workflow, the files to change, and a safe order for making changes.

The prompt rules live in both `skills/dream-to-video/SKILL.md` and `dream_to_video/prompt_engine.py`. Keep them aligned when you change prompt behavior. Platform-specific browser automation is concentrated in `dream_to_video/browser/engine.py`; queue orchestration and post-processing are in `dream_to_video/batch/worker.py`.

## License

[MIT](./LICENSE)
