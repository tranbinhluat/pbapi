# Repository Instructions for Codex Agents

These guidelines apply to the entire repository.

- Keep the codebase lightweight and dependency-free beyond the packages listed in `requirements.txt`.
- Add descriptive docstrings for all public classes and functions.
- Use type hints throughout the code.
- Update the README when user-facing functionality changes.
- Before committing, run the following syntax check:
  ```bash
  python -m py_compile powerbi_api_client/*.py examples/*.py
  ```
