---
name: systematic-debugging
description: Four-phase debugging methodology for Python applications. Use when debugging issues or investigating bugs.
---

# Systematic Debugging

## When to Use
- Investigating bugs
- Debugging test failures
- Root cause analysis
- Production incident response

## Four-Phase Process

### Phase 1: Reproduce
Establish a reliable reproduction of the issue.

```python
# Collect information
- Error message and stack trace
- Input that caused the failure
- Environment conditions
- Log entries around the time
```

### Phase 2: Hypothesize
Form testable hypotheses about the root cause.

```python
# Questions to ask
- What changed recently?
- When did it start failing?
- What are the failure patterns?
- Can I isolate the variable?
```

### Phase 3: Test
Test hypotheses methodically.

```python
# Add debugging
import pdb; pdb.set_trace()
print(f"DEBUG: {variable=}")

# Or use logging
import logging
logging.debug(f"State: {state}")
```

### Phase 4: Fix
Implement and verify the fix.

```python
# After fix
- Add regression test
- Document the root cause
- Review similar code
```

## Common Python Debugging Tools

```python
# Built-in
import pdb
pdb.set_trace()  # Set breakpoint

# Richer debugging
import ipdb
ipdb.set_trace()

# For async code
import aiomonitor
```

## Logging Pattern

```python
import logging
logger = logging.getLogger(__name__)

def process_data(data: dict) -> dict:
    logger.info(f"Processing data: {data.get('id')}")
    try:
        result = transform(data)
        logger.info(f"Success: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed: {e}", exc_info=True)
        raise
```

## Best Practices
- Never fix without understanding root cause
- Add tests to prevent regression
- Document what you learned
- Share findings with team
