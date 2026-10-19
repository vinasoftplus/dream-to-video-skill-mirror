# Customize This Workflow

This project turns a text description into a video-generation prompt, submits it through Jimeng in a browser, downloads the result, and optionally creates an effects version. Use this guide to adapt it without having to read the whole repository first.

## Workflow map

```text
Description
  -> agent skill instructions (`skills/dream-to-video/SKILL.md`)
  -> prompt transformation (`dream_to_video/prompt_engine.py`)
  -> task queue (`dream_to_video/batch/`)
  -> Jimeng browser integration (`dream_to_video/browser/`)
  -> download and post-processing (`dream_to_video/batch/worker.py`, `dream_to_video/effects/`)
  -> `dream_to_video/output/`
```

## Where to make changes

| If you want to change… | Start here | Also review |
| --- | --- | --- |
| What the agent asks for or returns | `skills/dream-to-video/SKILL.md` | README usage examples |
| How source descriptions become prompts | `dream_to_video/prompt_engine.py` | The prompt rules in `skills/dream-to-video/SKILL.md` |
| Video platform, login, submission, settings, or downloads | `dream_to_video/browser/engine.py` | `dream_to_video/browser/selectors.py` and `dream_to_video/batch/worker.py` |
| Queue behavior, retries, task matching, notifications | `dream_to_video/batch/worker.py` | `dream_to_video/batch/persistence.py` and `dream_to_video/models.py` |
| Reference image selection | `dream_to_video/browser/reference_image.py` | `dream_to_video/batch/worker.py` and `dream_to_video/reference_images/` |
| Output effects or formats | `dream_to_video/effects/` | `dream_to_video/batch/worker.py` |
| Runtime paths and settings | `dream_to_video/config.py` and `dream_to_video/.env.example` | `.gitignore` |

## Recommended first changes

1. Edit the skill's trigger description, input questions, prompt rules, and output instructions in `skills/dream-to-video/SKILL.md`.
2. Mirror prompt-generation rules in `dream_to_video/prompt_engine.py`. The skill and Python prompt are separate copies today, so changing only one can make interactive and queued runs behave differently.
3. Adjust generation behavior in `dream_to_video/browser/engine.py` only when the platform or its controls need to change. Keep platform-specific selectors in `dream_to_video/browser/selectors.py` where possible.
4. Change task lifecycle or output processing in `dream_to_video/batch/worker.py` when you need different retries, notifications, or post-processing.
5. Update `README.md` and `.env.example` to document new settings. Never commit `.env`, login state, API keys, or generated videos.

## Adding a different video platform

The current worker imports `JimengBrowser` directly, so platform changes touch orchestration as well as browser automation. For a small experiment, implement the new platform's login, submit, monitor, and download behavior alongside the current browser engine and select it in the worker. For a long-lived multi-platform fork, first define a narrow adapter contract (for example: `login`, `submit`, `wait_for_result`, and `download`) and make the worker depend on that contract rather than Jimeng-specific methods.

Keep platform settings, selectors, and authentication state separate. Avoid carrying cookies or browser profiles from one platform into another.

## Keeping a fork maintainable

- Keep your workflow changes in focused commits so upstream updates are easier to compare.
- Keep credentials, cookies, browser profiles, task databases, and output media out of version control; the existing `.gitignore` covers the default runtime folders.
- When changing prompt rules, inspect both copies noted above.
- When changing the browser flow, verify login, a single generation, download, and worker queue behavior against your account before relying on batch runs.
- Record new environment variables in `.env.example` with placeholder values only.

## Local setup

Follow [README.md](./README.md#setup) for installation. From the `dream_to_video` directory, copy `.env.example` to `.env`, add the API key for your chosen provider, install requirements, and sign in to Jimeng with `python main.py login`.
