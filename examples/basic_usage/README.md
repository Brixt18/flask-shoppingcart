# Basic usage — Test as_api.py

Quick instructions to run the example that exercises the library via `examples/basic_usage/as_api.py`.

Prerequisites
- Python installed (use a virtual environment recommended).
- pip available.

Steps
1. Open a terminal.
2. cd to the project root — the directory that contains both `examples` and `src` (you must be in this path).
3. (Optional) Create and activate a venv:
    - python -m venv .venv
    - On Windows: .venv\Scripts\activate
    - On macOS/Linux: source .venv/bin/activate
4. Install the package in editable mode:
    - python -m pip install -e .
5. Run the example:
    - python examples/basic_usage/as_api.py

Expected
- The example script will run using the locally installed package. You should see output or behavior defined by the example (no unhandled exceptions).

Troubleshooting
- If import errors occur, confirm you ran the install command from the project root.
- If dependencies are missing, inspect the package metadata (setup.cfg/pyproject.toml) and install as needed.
- To verify installation, run `python -c "import your_package_name; print(your_package_name.__version__)"` replacing with the package name.

That's all — run the two commands from the project root to test the example.