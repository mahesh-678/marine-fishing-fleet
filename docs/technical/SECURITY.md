# Security Notes

## Current implementation

- Flask-Login manages authenticated sessions.
- User passwords are stored as hashes using Werkzeug's password hashing helpers; the application verifies passwords against the stored hash.
- The `users.role` column supports `admin`, `organizer` and `viewer`.
- The `admin_required` decorator requires login and permits only `admin` or `organizer` for routes that modify operational data.
- Session cookies are configured as HTTP-only and SameSite Lax. The Secure flag is enabled when `APP_ENV=production`.
- Database credentials and secret configuration are read from environment variables. `.env` should remain local and must not be committed.

## Production recommendations

Before any public or operational deployment:

- Set a long, random `SECRET_KEY` and strong administrator password.
- Keep `.env`, database credentials and certificates out of Git.
- Use HTTPS and confirm secure cookie settings in production.
- Add and verify CSRF protection for state-changing forms.
- Review authorization for every route and API endpoint.
- Add login rate limiting, password reset procedures and account lifecycle controls.
- Restrict database network access and use a least-privilege database account.
- Back up the database and test restoration.
- Add audit logging for sensitive changes and monitor application errors.

This file documents the current prototype and recommended hardening; it is not a security certification.
