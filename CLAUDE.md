# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Activate virtual environment (Windows)
venv\Scripts\activate

# Run development server (port 5001, debug mode)
python app.py

# Run tests
pytest

# Run a single test file
pytest tests/test_auth.py

# Install dependencies
pip install -r requirements.txt
```

## Architecture

**Spendly** is a Flask server-rendered expense tracking app built as a step-by-step learning project. Students implement features incrementally across defined steps.

### Stack
- **Backend**: Flask 3.1.3 with Jinja2 templating
- **Database**: SQLite (accessed via `database/db.py`)
- **Frontend**: Vanilla HTML/CSS/JS — no build step, no npm
- **Testing**: pytest + pytest-flask

### Key Files
- `app.py` — all routes are defined here; placeholder routes are stubs for student steps
- `database/db.py` — students implement `get_db()`, `init_db()`, and `seed_db()` in Step 1
- `templates/base.html` — shared layout with navbar and footer; all pages extend this
- `static/css/style.css` — single stylesheet using CSS custom properties for the design system
- `static/js/main.js` — entry point for client-side JS (currently handles landing page video modal)

### Routing Convention
Routes follow REST-style URLs: `/expenses/<id>/edit`, `/expenses/<id>/delete`. The app runs on port `5001`.

### Design System
CSS custom properties are defined at `:root` in `style.css`:
- Colors: `--ink-*` (text tones), `--paper-*` (backgrounds), `--accent-green` (`#1a472a`), `--accent-orange` (`#c17f24`), `--danger`
- Fonts: DM Serif Display (headings), DM Sans (body) — loaded from Google Fonts in `base.html`
- Layout: `--max-width: 1200px`, `--auth-width: 440px`

### Implementation Steps
The project follows a numbered step plan embedded in `app.py` comments. Routes marked as placeholders (Steps 3–9) are stubs that students will flesh out — preserve these stub comments when editing.
