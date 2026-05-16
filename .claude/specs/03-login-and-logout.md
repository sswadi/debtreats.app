# Spec: Login and Logout

## Overview

Implement user authentication so registered users can sign in to and sign out of their Debtreats account. This step upgrades the existing stub `GET /login` route into a fully functional POST handler that verifies credentials against the `users` table and sets the Flask session. It also implements the `/logout` stub to clear the session. Together these routes gate all future authenticated features. A `login_required` decorator is introduced here so subsequent steps can protect their routes with a single annotation.

## Depends on

- Step 01 — Database setup (`users` table, `get_db()`)
- Step 02 — Registration (users exist in the DB to log in with)

## Routes

- `GET /login` — render the login form — public (already exists as stub, upgrade it)
- `POST /login` — verify email + password, set session, redirect to landing — public
- `GET /logout` — clear the session, redirect to `/login` — public (stub already exists, implement it)

## Database changes

No new tables or columns. Queries against the existing `users` table only.

A new DB helper should be added to `database/db.py`:

- `get_user_by_email(email)` — looks up a user row by email using a parameterised query, returns the row or `None`.

## Templates

- **Modify**: `templates/login.html`
  - Change the form `action` from the hardcoded string `/login` to `{{ url_for('login') }}`
  - Verify the existing `{% if error %}` block works correctly with the new POST route

## Files to change

- `app.py` — upgrade `login()` to handle `GET` and `POST`; implement `logout()`; add `login_required` decorator
- `database/db.py` — add `get_user_by_email()` helper
- `templates/login.html` — update form action to use `url_for('login')`

## Files to create

None.

## New dependencies

No new dependencies. Uses `werkzeug.security.check_password_hash` (already installed) and Flask's built-in `session`, `flash`, `redirect`, `url_for`.

## Rules for implementation

- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings in SQL
- Verify passwords with `werkzeug.security.check_password_hash` — never compare plaintext
- On failed login (wrong email or wrong password), re-render `login.html` with a generic error: `"Invalid email or password."` — do not reveal which field is wrong (prevents user enumeration)
- On successful login, set `session["user_id"]` and `session["user_name"]`, flash a welcome message, and `redirect` to `url_for("landing")`
- `logout()` must call `session.clear()` (not just pop individual keys), flash a sign-out confirmation message, and `redirect` to `url_for("login")`
- The `login_required` decorator must redirect unauthenticated requests to `url_for("login")` with a flashed info message; preserve the decorator with `functools.wraps`
- All templates extend `base.html`
- Use CSS variables — never hardcode hex values
- Use `url_for()` for every internal link — never hardcode URLs

## Definition of done

- [ ] `GET /login` renders the login form without errors
- [ ] Submitting with correct credentials sets `session["user_id"]` and `session["user_name"]`, flashes a welcome message, and redirects to the landing page
- [ ] Submitting with a wrong password re-renders the form with `"Invalid email or password."` — no session is set
- [ ] Submitting with an unregistered email re-renders the form with `"Invalid email or password."` — no session is set
- [ ] `GET /logout` clears the entire session and redirects to `/login` with a signed-out flash message
- [ ] The navbar shows the user's name and "Sign out" link when logged in (wired in `base.html` — verify it renders correctly after login)
- [ ] The navbar shows "Sign in" and "Get started" links when no session is active
- [ ] A route decorated with `login_required` redirects an unauthenticated request to `/login`
