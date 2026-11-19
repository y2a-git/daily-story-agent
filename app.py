import os
from pathlib import Path
from dotenv import load_dotenv, set_key
import streamlit as st

from story_engine import (
    BASE_DIR,
    ENV_PATH,
    OUTPUT_ROOT,
    ensure_env_file,
    run_daily_story,
)

st.set_page_config(
    page_title="Daily English Story & Art Agent",
    page_icon="📖",
    layout="centered",
)

ensure_env_file()
load_dotenv(dotenv_path=ENV_PATH, override=True)

st.title("📖 Daily English Story & Art Agent")
st.write(
    "Get a fresh English short story with a custom illustration every day. "
    "Save your API key once in the sidebar, pick a story style, and click **Generate Today's Story**."
)

# Sidebar setup for non-technical users
with st.sidebar:
    st.header("1. Setup (One-Time)")
    current_key = os.getenv("OPENAI_API_KEY", "")
    display_key = "" if current_key == "your_api_key_here" else current_key

    api_key_input = st.text_input(
        "OpenAI API Key",
        value=display_key,
        type="password",
        help="Paste your OpenAI API key starting with sk-. It stays saved locally in your .env file.",
    )

    if st.button("Save API Key"):
        cleaned_key = api_key_input.strip()
        if not cleaned_key:
            st.error("Please paste an API key before saving.")
        else:
            set_key(str(ENV_PATH), "OPENAI_API_KEY", cleaned_key)
            os.environ["OPENAI_API_KEY"] = cleaned_key
            st.success("API key saved locally to .env!")

    st.divider()
    st.header("2. Story Style")
    style = st.selectbox(
        "Choose a vibe",
        options=[
            "cozy storybook",
            "gentle bedtime fable",
            "curious sci-fi adventure",
            "magical mystery",
            "humorous slice-of-life",
        ],
        index=0,
    )

# Main action button
if st.button("✨ Generate Today's Story", type="primary", use_container_width=True):
    with st.spinner("Writing your story and painting the illustration..."):
        try:
            result = run_daily_story(style=style)
            st.success(f"Saved for {result['date']}!")
        except Exception as exc:
            st.error(str(exc))

st.divider()
st.subheader("Past & Today's Stories")

if OUTPUT_ROOT.exists():
    story_dirs = sorted(
        [p for p in OUTPUT_ROOT.iterdir() if p.is_dir() and (p / "story.md").exists()],
        key=lambda p: p.name,
        reverse=True,
    )
else:
    story_dirs = []

if not story_dirs:
    st.info("No stories generated yet. Click **Generate Today's Story** above to create your first one.")
else:
    selected_dir = st.selectbox(
        "Select a story date",
        options=story_dirs,
        format_func=lambda p: p.name,
    )
    md_text = (selected_dir / "story.md").read_text(encoding="utf-8")
    image_file = selected_dir / "scene_1.png"

    lines = md_text.splitlines()
    title = lines[0].lstrip("# ").strip() if lines and lines[0].startswith("#") else selected_dir.name
    body_lines = [
        line for line in lines[1:]
        if not line.strip().startswith("![")
    ]
    story_body = "\n".join(body_lines).strip()

    st.markdown(f"### {title}")
    if image_file.exists():
        st.image(str(image_file), use_container_width=True)
    st.markdown(story_body)