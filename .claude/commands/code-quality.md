---
description: Run quality checks on the codebase
allowed-tools: Bash(ruff:*), Bash(pytest:*), Read
---

# Code Quality Command

Your task is to run quality checks and report findings.

## Steps

1. **Run linting**: `ruff check .`
2. **Run type checking**: `pyright --pythonversion 3.11 .`
3. **Run tests**: `pytest --cov=src --cov-report=term-missing`
4. **Check formatting**: `ruff format --check .`

## Report Format

```
## Code Quality Report

### Linting
- Status: PASS/FAIL
- Issues: [list]

### Type Checking
- Status: PASS/FAIL
- Errors: [list]

### Tests
- Coverage: XX%
- Status: PASS/FAIL

### Formatting
- Status: PASS/FAIL
