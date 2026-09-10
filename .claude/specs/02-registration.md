# Spec: Registration

## Overview
This step implements the actual account-creation logic behind the existing `/register` page. Right now `GET /register` only renders a static form — there is no `POST` handler, so submitting the form does nothing. This step adds `POST /register`, which validates the submitted data, hashes the password, and inserts a new row into `users`. On success the user does not get auto-logged-in — they're shown a success message and redirected to the login page to sign in. Session-based authentication (needed for Step 3 logout and Step 4 profile) is deferred to whichever future step implements `POST /login`.

## Depends on
- Step 1 — Database setup (`users` table, `get_db()`, `init_db()`)

## Routes
- `POST /register` — process the registration form: validate input, check for duplicate email, hash the password, insert the user, flash a success message, redirect to `/login` — public
- `GET /register` — already implemented, unchanged (still renders `register.html`, now also re-renders it with an error message on validation failure)

## Database changes
No database changes. The existing `users` table (`id`, `name`, `email`, `password_hash`, `created_at`) already supports registration as defined in `database/db.py`.

New functions needed in `database/db.py` (logic only, no schema change):
- `get_user_by_email(email)` — returns the user row matching an email, or `None`
- `create_user(name, email, password_hash)` — inserts a new user row and returns the new `id`

## Templates
- **Create:** none
- **Modify:** `templates/register.html` — fix hardcoded `action="/register"` to use `{{ url_for('register') }}`; repopulate `name`/`email` field values on validation error instead of clearing the form; add a `confirm_password` field with an inline "Passwords do not match." message that is highlighted (red border + red text) both live client-side and on a server-rendered mismatch

## Files to change
- `app.py` — add `secret_key` config (needed for `flash()`), add `POST` handling to the `/register` route (validation, calling `database/db.py` helpers, flashing a success message, redirecting to `/login`)
- `database/db.py` — add `get_user_by_email()` and `create_user()`
- `templates/register.html` — fix hardcoded form action, repopulate fields on error, add the `confirm_password` field and its inline error markup
- `templates/login.html` — render the flashed success message
- `static/css/style.css` — add `.auth-success` styling, `.input-error` (red border) and `.field-error` (red inline text) styling
- `static/js/main.js` — vanilla JS to live-validate that `password` and `confirm_password` match, toggling the red border/text as the user types and blocking submission on mismatch (client-side UX only — the server still validates independently)

## Files to create
None

## New dependencies
No new dependencies. Uses Flask's built-in `flash()` / `get_flashed_messages()` (signed session cookie under the hood) to pass the success message across the redirect — no Flask-Login or other auth package, and no login session is created.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`generate_password_hash` / `check_password_hash`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- All DB access for the new logic lives in `database/db.py`, not inline in `app.py`
- Validate server-side even though the form has HTML5 `required`/`type` attributes and client-side JS checks: name non-empty, email non-empty and well-formed, password at least 8 characters, `password` matches `confirm_password`, email not already registered ("Account already exists.")
- Client-side JS validation of the password/confirm-password match is a UX convenience only — never trust it in place of the server-side check
- On any validation failure, re-render `register.html` with a single `error` message and HTTP 400 — do not redirect
- On success, do not auto-login — flash a success message and redirect to `/login`. No session/`user_id` is set at registration time
- Do not implement `POST /login`, `GET /logout`, or the real `/profile` page — those are later steps and must remain untouched stubs

## Definition of done
- [ ] `GET /register` still renders the form with no errors
- [ ] The form has a `confirm_password` field in addition to `name`, `email`, `password`
- [ ] Submitting valid name/email/password/confirm_password creates a new row in `users` with a hashed (not plaintext) password
- [ ] Typing a `confirm_password` that doesn't match `password` highlights the field's border red and shows "Passwords do not match." inline, live, without submitting the form
- [ ] Submitting a mismatched `password`/`confirm_password` directly (e.g. via curl, bypassing the client-side JS) is still rejected server-side with the same message, HTTP 400, and no row inserted
- [ ] Submitting an email that already exists shows "Account already exists." inline and does not insert a duplicate row
- [ ] Submitting an empty name, invalid email, or password under 8 characters shows an inline error and does not insert a row
- [ ] On successful registration, a success message is flashed and the response redirects to `/login` (no session/`user_id` is set)
- [ ] Reloading `/register` after a validation error keeps the previously entered name and email in the form fields (password and confirm password are never repopulated)
- [ ] `app.py` contains no inline SQL — all queries go through `database/db.py`
- [ ] `requirements.txt` is unchanged
