"""Google Veo video generation using the Gemini Developer API."""

import asyncio
from datetime import datetime
from pathlib import Path
import time

from config import (
    GEMINI_API_KEY,
    GENERATION_TIMEOUT,
    OUTPUT_DIR,
    VEO_MODEL,
    VEO_POLL_INTERVAL,
)


async def generate_video(prompt: str) -> Path:
    """Generate one Veo video and save its MP4 under the project's output directory."""
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is required for Veo. Add a Gemini API key to dream_to_video/.env."
        )

    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:
        raise RuntimeError(
            "The Google Gen AI SDK is missing. Install requirements with: "
            "pip install -r requirements.txt"
        ) from exc

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output_path = OUTPUT_DIR / f"veo_{stamp}.mp4"

    client = genai.Client(api_key=GEMINI_API_KEY)
    try:
        print(f"🎬 Submitting prompt to Veo ({VEO_MODEL})...")
        operation = await asyncio.to_thread(
            client.models.generate_videos,
            model=VEO_MODEL,
            prompt=prompt,
            config=types.GenerateVideosConfig(number_of_videos=1),
        )

        print("⏳ Veo is generating the video...")
        deadline = time.monotonic() + GENERATION_TIMEOUT
        while not operation.done:
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    f"Veo generation did not finish within {GENERATION_TIMEOUT} seconds."
                )
            await asyncio.sleep(VEO_POLL_INTERVAL)
            operation = await asyncio.to_thread(client.operations.get, operation)

        operation_error = getattr(operation, "error", None)
        if operation_error:
            raise RuntimeError(str(operation_error))

        response = getattr(operation, "response", None)
        generated_videos = getattr(response, "generated_videos", None) or []
        if not generated_videos:
            raise RuntimeError("Veo completed without returning a video.")

        generated_video = generated_videos[0]
        await asyncio.to_thread(
            client.files.download,
            file=generated_video.video,
            destination=str(output_path),
        )
        if not output_path.is_file():
            raise RuntimeError("The Veo download completed without creating an output file.")

        return output_path
    finally:
        await asyncio.to_thread(client.close)
