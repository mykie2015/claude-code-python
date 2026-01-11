---
description: Review changes and create PR description
allowed-tools: Bash(git:*), Read, Grep
---

# PR Review Command

Your task is to review pending changes and generate a PR summary.

## Steps

1. Run `git diff main...HEAD` to see all changes
2. Review each modified file
3. Check for common issues:
   - Missing type hints
   - No tests for new functionality
   - Hardcoded values that should be constants
   - Missing error handling
4. Generate a PR description

## PR Description Template

```
## Summary
[Brief description of changes]

## Changes
- [List of key changes]

## Testing
- [Tests added/modified]
- [Coverage impact]

## Notes
- [Known limitations]
- [Breaking changes]
```

Current branch: !`git branch --show-current`
Recent commits: !`git log --oneline -5`
