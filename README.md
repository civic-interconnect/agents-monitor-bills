# agents-monitor-bills


> Bill Monitor Agent for Civic Interconnect

[![Version](https://img.shields.io/badge/version-v0.2.0-blue)](https://github.com/civic-interconnect/agents-monitor-bills/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/civic-interconnect/agents-monitor-bills/actions/workflows/agent-runner.yml/badge.svg)](https://github.com/civic-interconnect/agents-monitor-bills/actions)

This agent queries basic bill metadata from OpenStates using their GraphQL API.
It creates daily snapshot reports of bill counts by jurisdiction to help track overall system volume and schema stability

## Current Status

- Pulls OpenStates bills via GraphQL (high-level bill IDs only)
- Generates daily jurisdiction-level summary reports
- Introspection/schema monitoring not yet enabled
- Deeper bill content monitoring (texts, sponsors, versions, etc.) not yet implemented

## Local development

```powershell
py -m venv .venv
.\.venv\Scripts\activate
py -m pip uninstall civic-lib -y
py -m pip install --upgrade pip setuptools wheel --prefer-binary
py -m pip install --upgrade -r requirements-dev.txt --timeout 100 --no-cache-dir
pre-commit install
py main.py
```

## Deployment

This agent is scheduled to run automatically using GitHub Actions.

## Before Starting Changes

```shell
git pull
```

## After Tested Changes (New Version Release)

First: Update these files to the new version:

1. VERSION file
2. README.md (update version badge)

Then run the following:

```shell
pre-commit autoupdate --repo https://github.com/pre-commit/pre-commit-hooks
ruff check . --fix
git add .
git commit -m "Release v0.2.0: Sync all agents with civic-lib v0.9.0"
git push origin main
git tag v0.2.0
git push origin v0.2.0
```
