# Garden Prompt Generator

A desktop app built with **Python and Tkinter** to generate **photorealistic Japanese garden prompts** and **SEO-optimized YouTube titles/descriptions** — perfect for lo-fi music creators, aesthetic YouTubers, or chill visual artists.

---

## Features

- **Image Prompt Generator**  
  Generate cinematic and photorealistic prompts like
  "a fog-kissed Japanese garden under lantern light, with dew-covered bonsai and mossy footpaths..."
  Use with tools like Midjourney, DALL·E, or ChatGPT's built-in image model.

- **Title Generator**  
  Instantly generate unique title combinations with categories like Japanese, Chinese, and Rain-Themed words.  
  Save, copy, delete, and even prepare SEO-ready prompts for ChatGPT with a single click.

- **Music Prompt Generator**  
  Generate text prompts for local music generation models (e.g., MusicGen, Riffusion, etc).
  Great for creating chill background tracks or ambient loops based on natural aesthetics.

  ⚠️ Requires a local AI music model installed on your machine.
  This app does not generate audio by itself — it prepares prompts to use in your preferred model.

- **Main Launcher GUI**  
  A clean start screen that lets you launch either generator in separate tabs — no coding knowledge required.

- **Light/Dark Mode** toggle

---
### Project Structure

- `ImagePromptGenerator/`
  - `gui_prompt_generator.py` — GUI for image prompt generation

- `TitleGenerator/`
  - `main_title_generator_gui.py` — GUI for title + SEO helper
  - `thumbnail_title_word_lists.csv` — CSV source for title generation

- `Launcher/`
  - `main_launcher.py` — Launches the main GUI with tabs

- `.gitignore`
- `README.md`




## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/seb-kvist/Garden-Prompt-Generator.git
cd Garden-Prompt-Generator/Launcher
```

### 2. Set up a virtual environment (optional but recommended)
```bash
python -m venv env
source env/bin/activate    # On Windows: env\Scripts\activate
```

### 3. Install requirements
```bash
pip install -r requirements.txt
```
### 4. Run the app
```bash
python main_launcher.py
```
## SEO Prompt Helper
In the Title Generator, you can click a button to create a ready-to-paste SEO prompt that looks like this:
```bash
I want you to give me SEO optimized for [Title Here]. The description:

I want you to follow these rules when getting SEO:

1. SEO-Optimized YouTube Title
Titles should include keywords like: Lo-Fi, Chill Beats, Japanese/Chinese Garden, Zen, Relaxing, Study, Sleep, Meditation, etc.
Include the [Title Here]
Clickable, clear, and not repetitive
Use fitting natural emojis

2. YouTube Description
3–5 aesthetic sentences
Tone: poetic and peaceful
Include this line on its own:
👉 [Youtube Channel here]
No mention of livestreams

3. Tags
Up to 500 characters
No hashtags

4. Pinned Comment Suggestion
Welcoming tone, ask a question to invite comments

```
## Screenshots
| Launcher                       | Title Generator            | Image Prompt                |
| ------------------------------ | -------------------------- | --------------------------- |
| ![Launcher](docs/launcher.png) | ![Titles](docs/titles.png) | ![Prompt](docs/prompts.png) |

## Tech Stack
- Python 3.10+
- Tkinter
- Pandas (for CSV)
- Designed for local use, no external APIs needed

## License
MIT License — Free to use, modify and contribute.
If you enjoy this project, ⭐️ it on GitHub or share it!
