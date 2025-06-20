# agents-monitor-bills


> Bill Monitor Agent for Civic Interconnect

[![Version](https://img.shields.io/badge/version-v0.2.1-blue)](https://github.com/civic-interconnect/agents-monitor-bills/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/civic-interconnect/agents-monitor-bills/actions/workflows/agent-runner.yml/badge.svg)](https://github.com/civic-interconnect/agents-monitor-bills/actions)

This agent queries basic bill metadata from OpenStates using their GraphQL API.
It creates daily snapshot reports of bill counts by jurisdiction to help track overall system volume and schema stability

## Current Status

- Pulls OpenStates bills via GraphQL (high-level bill IDs only)
- Generates daily jurisdiction-level summary reports
- Introspection/schema monitoring not yet enabled
- Deeper bill content monitoring (texts, sponsors, versions, etc.) not yet implemented

## Deployment

This agent is scheduled to run automatically using GitHub Actions.

## Local Development

See [REF_DEV.md](./REF_DEV.md). Then:

```shell
py main.py
```
