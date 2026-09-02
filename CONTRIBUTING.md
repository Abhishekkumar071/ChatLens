# Contributing to ChatLens

Thanks for considering contributing! Here's how to get started:

## Setup
1. Fork and clone the repo
2. `python -m venv .venv` and activate it
3. `pip install -r requirements.txt`
4. `pytest -v` to confirm the existing test suite passes

## Making changes
- Keep changes focused — one feature/fix per pull request
- Add tests for new parsing logic or data transformations
- Run `ruff check .` before committing
- Follow the existing modular structure: parsers/ for platform parsing, processing/ for data transforms, ui/ for tab rendering

## Submitting
1. Create a branch: `git checkout -b feature/your-feature-name`
2. Commit with a clear message
3. Push and open a Pull Request against `main`

CI will automatically run tests and linting on your PR.