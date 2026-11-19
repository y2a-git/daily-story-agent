import base64
import json
import os
import shutil
from datetime import date
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
ENV_EXAMPLE_PATH = BASE_DIR / ".env.example"
STATE_PATH = BASE_DIR / "state.json"
OUTPUT_ROOT = BASE_DIR / "stories"


def ensure_env_file() -> None:
    if not ENV_PATH.exists() and ENV_EXAMPLE_PATH.exists():
        shutil.copy(ENV_EXAMPLE_PATH, ENV_PATH)
    load_dotenv(dotenv_path=ENV_PATH, override=True)


def get_client() -> OpenAI:
    ensure_env_file()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key or api_key == "your_api_key_here":
        raise ValueError(
            "No OpenAI API key found yet. Please paste your API key in the setup box "
            "or inside the .env file so the app can create stories and images."
        )
    return OpenAI(api_key=api_key)


def load_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {"recent_themes": []}


def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


def generate_story_and_prompt(recent_themes: list[str], style: str = "cozy storybook") -> dict:
    client = get_client()
    avoid_text = ", ".join(recent_themes[-10:]) or "none"
    try:
        response = client.responses.create(
            model="gpt-6-luna",
            input=(
                f"Write a warm, engaging English short story (300-450 words) in a '{style}' style "
                "with a clear beginning, middle, and ending. Also write one vivid illustration prompt "
                "for a key scene (watercolor and ink storybook illustration, no text or words in the image). "
                f"Avoid these recent themes: {avoid_text}.\n"
                "Return valid JSON only with keys: title, theme, story, image_prompt."
            ),
        )
        raw = response.output_text.strip()
        if raw.startswith("```"):
            raw = raw.strip("`").removeprefix("json").strip()
        return json.loads(raw)
    except OpenAIError as exc:
        raise RuntimeError(
            f"Could not generate the story right now. Check your API key and billing/quota status. Details: {exc}"
        ) from exc


def generate_illustration(prompt: str, output_path: Path) -> None:
    client = get_client()
    try:
        result = client.images.generate(
            model="gpt-image-2.6-flare",
            prompt=prompt,
            size="1536x1024",
            quality="low",
        )
        image_bytes = base64.b64decode(result.data[0].b64_json)
        output_path.write_bytes(image_bytes)
    except OpenAIError as exc:
        raise RuntimeError(
            f"The story was written, but image generation hit an issue. Check your API key/quota. Details: {exc}"
        ) from exc


def run_daily_story(style: str = "cozy storybook") -> dict:
    today = date.today().isoformat()
    day_dir = OUTPUT_ROOT / today
    day_dir.mkdir(parents=True, exist_ok=True)

    state = load_state()
    payload = generate_story_and_prompt(state["recent_themes"], style=style)

    image_path = day_dir / "scene_1.png"
    generate_illustration(payload["image_prompt"], image_path)

    story_md = day_dir / "story.md"
    story_md.write_text(
        f"# {payload['title']}\n\n![Story Illustration](scene_1.png)\n\n{payload['story']}\n",
        encoding="utf-8",
    )

    state["recent_themes"].append(payload["theme"])
    save_state(state)

    return {
        "date": today,
        "title": payload["title"],
        "story": payload["story"],
        "image_path": str(image_path),
        "markdown_path": str(story_md),
    }