# Daily English Story & Art Agent

A beginner-friendly app that writes a fresh **English short story** with a **custom illustration** and opens a simple reading page in your web browser.

## Before You Start (What You Need)

1. **Python 3.10 or newer** installed on your computer:
   - Download from [python.org/downloads](https://www.python.org/downloads/).
   - **Windows users:** Check **"Add python.exe to PATH"** on the first installer screen.
2. **An OpenAI API key** with billing/credits enabled:
   - Create one at [platform.openai.com](https://platform.openai.com/).
   - Each story + illustration uses your own API key and costs only a few cents per run.

---

## How to Install & Run (No Coding Required)

### Step 1: Download the Project
1. Click the green **Code** button on this GitHub page and select **Download ZIP**.
2. Extract (unzip) the folder onto your Desktop or Documents folder.

### Step 2: Double-Click to Launch
- **Windows:** Open the extracted folder and double-click **`start_windows.bat`**.
- **Mac / Linux:** Open the extracted folder and double-click **`start_mac_linux.command`** (if macOS asks for permission in Security & Privacy, allow it to open).

The first run sets up a private local folder (`.venv`) and installs the needed tools automatically. Your web browser will open to the app.

### Step 3: Add Your API Key & Generate a Story
1. In the left sidebar, paste your **OpenAI API Key** and click **Save API Key**.
2. Pick a **Story Style** (such as *cozy storybook* or *gentle bedtime fable*).
3. Click **✨ Generate Today's Story**.

Stories and images are saved locally inside the `stories/` folder so you can re-read them anytime.

---

## Troubleshooting

- **"No OpenAI API key found yet":** Paste a valid key starting with `sk-` into the sidebar and click **Save API Key**.
- **Quota or billing error:** Make sure your OpenAI account has active billing/credits enabled.
- **Browser didn't open automatically:** Look at the terminal window for a link like `http://localhost:8501` and open it in Chrome, Safari, Edge, or Firefox.

## Privacy & Safety Note
- Your API key is stored only on your own computer in `.env` (which is ignored by Git). Never share your `.env` file or API key with anyone.