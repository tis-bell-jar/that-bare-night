# Flask Notes Web Application

A simple notes app built with Flask. Users can create an account, log in and manage plain text notes. Data is stored in a local SQLite database via SQLAlchemy.

## Live site

<https://notesapp-rad4.onrender.com>

## Current features

- User registration and authentication using **Flask-Login**.
- Add new notes from the home page.
- Delete existing notes without leaving the page (uses a small JavaScript helper).
- Bootstrap based templates for basic styling.

## Planned features

The repository contains placeholders for upcoming work:

- Ability to tag notes (`tag_api.py`).
- Editing existing notes.
- Unit tests for the API.

## Setup

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Set required environment variables:

   - `SECRET_KEY` – secret value used by Flask to sign session cookies. If not set,
     a default development key is used from `website/__init__.py`.
   - `FLASK_APP` – set to `main.py` when using the `flask run` command.
   - `FLASK_ENV` – optional, set to `development` to enable debug mode.

   Example:

   ```bash
   export SECRET_KEY="change-me"
   export FLASK_APP=main.py
   export FLASK_ENV=development
   ```

3. Initialize the SQLite database and start the development server:

   ```bash
   python main.py
   ```

   or with `flask run` after exporting `FLASK_APP`.

## Running tests

Tests are written with `pytest` (currently mostly placeholders). Run them with:

```bash
pytest -q
```

