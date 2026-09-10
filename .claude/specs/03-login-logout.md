# Spec: Login and Logout

## Overview
This step implements real session-based authentication for Spendly. `GET /login` already renders `login.html`, but there is no `POST /login` handler, so the form does nothing — users cannot actually sign in. `GET /logout` is still a raw-string stub. This step adds the `POST /login` handler (verify email/password against the `users` table, start a session), implements `GET /logout` (clear the session, redirect to login), and updates `base.html` to reflect logged-in state in the navbar. This is the step that finally makes the accounts created in Step 2 usable, and it lays the session foundation that Step 4 (`/profile`) and all later expense routes will depend on for identifying the current user.

## Depends on
- Step 1 — Database setup (`users` table, `get_db()`, `init_db()`)
- Step 2 — Registration (`get_user_by_email()`, `create_user()`, existing `password_hash` column)

## Routes
- `POST /login` — validate email/password against `users`, verify with `check_password_hash`, on success store `user_id` in `session` and redirect to `/`; on failure re-render `login.html` with an error and the submitted email repopulated — public
- `GET /logout` — clear the session (`session.clear()`) and redirect to `/` — logged-in

`GET /login` and `GET /register` are unchanged (already implemented in prior steps).

## Database changes
No database changes. The existing `users` table (`id`, `name`, `email`, `password_hash`, `created_at`) already has everything needed to authenticate — no new tables or columns required.

## Templates
- **Create:** None
- **Modify:**
  - `templates/login.html` — change the hardcoded `action="/login"` to `action="{{ url_for('login') }}"`; add an `{% if error %}` error block matching the pattern already used in `register.html`; repopulate the `email` field's `value` on a failed submit
  - `templates/base.html` — in the navbar, conditionally show a "Logout" link (`url_for('logout')`) when `session.get('user_id')` is set, instead of always showing "Sign in" / "Get started"

## Files to change
- `app.py` — add `POST` handling to the `login` route, implement `logout`, import `check_password_hash` and `session` from `flask`/`werkzeug.security`
- `templates/login.html`
- `templates/base.html`
- `CLAUDE.md` — update the route table to mark `GET /logout` as implemented

## Files to create
None.

## New dependencies
No new dependencies. Session support uses Flask's built-in `session` object (already backed by `app.secret_key` in `app.py`); password verification uses `werkzeug.security.check_password_hash`, already available via the existing `werkzeug` dependency.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`check_password_hash` against the stored `password_hash` — never compare plaintext)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- No DB logic inline in `app.py` — reuse `get_user_by_email()` from `database/db.py`; do not add new DB logic to `login`/`logout` beyond that existing lookup
- Do not implement `/profile`, `/expenses/add`, `/expenses/<id>/edit`, or `/expenses/<id>/delete` — those remain stubs for later steps
- Do not auto-expire or add "remember me" / persistent-session behavior — a plain Flask session cookie is sufficient for this step

## Definition of done
- [ ] Visiting `/login` and submitting the seeded demo credentials (`demo@spendly.com` / `demo123`) redirects to `/` and sets a session cookie
- [ ] Submitting `/login` with a wrong password re-renders `login.html` with an error message and the email field still filled in, and does not create a session
- [ ] Submitting `/login` with an email that doesn't exist in `users` shows the same generic error (no distinction between "wrong password" and "no such user")
- [ ] After logging in, visiting `/logout` clears the session and redirects to `/`
- [ ] After `/logout`, the navbar shows "Sign in" / "Get started" again instead of "Logout"
- [ ] While logged in, the navbar shows a "Logout" link instead of "Sign in" / "Get started"
- [ ] No plaintext password ever appears in a query, log, or template
- [ ] `pytest` passes with no regressions to existing registration tests (if any exist)
