# DEVELOPER.md

## Setup for Running Agent

1. Fork the repo.
2. Clone your fork and open it in VS Code.
3. Open a terminal (examples below use PowerShell on Windows).

```powershell
git clone https://github.com/civic-interconnect/agents-monitor-bills.git
cd agents-monitor-bills

py -m venv .venv
.\.venv\Scripts\activate
py -m pip install --upgrade pip setuptools wheel --prefer-binary
py -m pip install -e .[dev]
bills-agent start
```

## Publish API

```powershell
civic-dev publish-api
mkdocs serve
```

## Releasing New Version

Before publishing a new version, delete .venv. and recreate and activate.
Run pre-release preparation, installing and upgrading without the -e editable flag.
Verify all tests pass. Run prep-code (twice if needed).
Verify the docs are generated and appear correctly.

```powershell
git pull
py -m venv .venv
.\.venv\Scripts\activate
py -m pip install --upgrade pip setuptools wheel --prefer-binary
py -m pip install --upgrade .[dev]
pytest tests
civic-dev prep-code
civic-dev publish-api
mkdocs serve
civic-dev bump-version 0.2.4 0.2.5
civic-dev release
```
