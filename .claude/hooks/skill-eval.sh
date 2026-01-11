#!/bin/bash
# Skill evaluation hook - suggests skills based on prompt analysis

PROMPT="$1"

if echo "$PROMPT" | grep -qiE "test|pytest|fixture|mock"; then
    echo "SKILL SUGGESTION: python-testing - Keywords matched: test/pytest"
fi

if echo "$PROMPT" | grep -qiE "api|endpoint|fastapi|route|request|response"; then
    echo "SKILL SUGGESTION: fastapi-patterns - Keywords matched: api/fastapi"
fi

if echo "$PROMPT" | grep -qiE "debug|bug|error|issue|investigate|trace"; then
    echo "SKILL SUGGESTION: systematic-debugging - Keywords matched: debug/bug"
fi

exit 0
