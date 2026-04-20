# ML Portfolio Generator

A FastAPI app that turns a resume PDF into a simple personal portfolio site using NLP and summarization.

The app:

- extracts text from an uploaded PDF resume
- generates a short bio with a Hugging Face summarization model
- pulls out likely skills with spaCy
- injects the results into a themed HTML/CSS portfolio template
- writes the generated site into `generated_sites/`

## Features

- Resume PDF upload
- AI-generated professional bio
- Automatic skill extraction
- Multiple visual themes: `neo`, `glass`, and `gloss`
- Custom primary color selection
- Static HTML/CSS output for each generated portfolio

## Tech Stack

- Python
- FastAPI
- Uvicorn
- PyMuPDF
- spaCy
- Hugging Face Transformers
- Torch

## Project Structure

```text
.
├── main.py
├── init_project.py
├── requirements.txt
├── templates/
│   ├── index.html
│   └── preview_wrapper.html
├── static/
│   ├── style.css
│   └── preview.css
├── portfolio_templates/
│   ├── neo/
│   ├── glass/
│   └── gloss/
└── generated_sites/
```

## Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python3 main.py
```

4. Open the app in your browser:

```text
http://127.0.0.1:8000
```

## First Run Notes

- The app loads the spaCy model `en_core_web_sm`.
- If that model is not installed, `main.py` attempts to download it automatically.
- The summarizer uses `sshleifer/distilbart-cnn-12-6`, which may take a moment to download on first run.

## How It Works

1. Upload a PDF resume from the home page.
2. Choose a theme and primary color.
3. The backend extracts text with PyMuPDF.
4. spaCy identifies candidate skill terms from the resume text.
5. Transformers generates a short summary for the portfolio bio.
6. The selected HTML/CSS template is populated and saved into `generated_sites/job_<id>/`.

## Output

Each generated portfolio creates:

- `generated_sites/job_<id>/index.html`
- `generated_sites/job_<id>/style.css`
- `generated_sites/job_<id>.zip`

## Available Themes

- `neo`: bold neo-brutalist layout
- `glass`: glassmorphism card layout
- `gloss`: glossy modern layout

## API

### `GET /`

Serves the main upload interface.

### `POST /generate`

Accepts:

- `file`: PDF resume
- `theme`: one of `neo`, `glass`, `gloss`
- `primary_color`: hex color value such as `#00d2ff`

Returns JSON similar to:

```json
{
  "preview_url": "/preview/job_abc123",
  "job_id": "job_abc123"
}
```

## Current Limitations

- `main.py` currently defines `GET /` and `POST /generate` only.
- The frontend references preview and download routes, but those endpoints are not implemented in the current backend file.
- The generated portfolio name is currently hardcoded as `Professional Portfolio`.
- Skill extraction is heuristic-based and may include noisy nouns from the resume text.

## Initialization Script

`init_project.py` creates a basic starter structure and writes initial template files for the `neo` and `glass` themes.

## Ideas For Improvement

- add working preview and download endpoints
- extract the candidate's real name from the resume
- improve skill filtering and deduplication
- support more themes and richer template customization
- add tests for parsing and generation flows

## License

No license file is currently included in this repository.
