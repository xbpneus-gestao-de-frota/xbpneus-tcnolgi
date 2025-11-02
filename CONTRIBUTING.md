# Contributing to XBPneus

Thank you for contributing! This project uses a multi‑tenant architecture and a combination of Django (backend), React (frontend) and other services. To keep the codebase stable and secure, follow these guidelines before opening a pull request.

## Getting started

1. Fork this repository and clone your fork locally.
2. Copy `.env.example` to `.env` and set the required environment variables for your local environment. **Never commit `.env` with real credentials**—this file is meant to remain private.
3. Install dependencies for both the backend and frontend:
   ```sh
   # Backend
   cd backend
   pip install -r requirements.txt

   # Frontend
   cd ../frontend
   npm install
   ```
4. Run the development servers and ensure the application starts without errors.

## Coding standards

- **Use pre‑commit hooks**: This repository includes a `.pre-commit-config.yaml` (see below). Run `pre-commit install` after cloning so that Black, Flake8, ESLint and Prettier run automatically on staged files.
- Keep code style consistent with Black (Python) and Prettier (JS/TS). Lint errors will cause CI to fail.
- Follow the architectural conventions described in `CHANGES_XBPNEUS.txt` (e.g., keep `rest_framework`, `corsheaders`, `rest_framework_simplejwt` in `INSTALLED_APPS`, use `/api/<app>` for API routes, and standardize labels like "Borracharia").
- Write tests for any new feature or bugfix. Backend tests use pytest; frontend tests use Jest/React Testing Library. Playwright specs live under `e2e/`.

## Opening a pull request

- Create a descriptive branch name and open a pull request against `main`.
- Ensure the CI pipeline passes (`lint-test.yml` runs lint and tests).
- If your change adds new environment variables, update `.env.example` accordingly and document them in the PR description.
- Assign reviewers as appropriate; code owners may be requested automatically.

## Security

- Do not commit any secrets, passwords or API keys. Use environment variables and secret managers.
- Respect the multi‑tenant boundaries; never mix data between tenants.

Thank you for helping make XBPneus better!
