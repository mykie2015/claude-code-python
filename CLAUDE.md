# Python Project

## Quick Facts

- **Stack**: Python 3.11+, FastAPI/pytest
- **Test Command**: `pytest`
- **Lint Command**: `ruff check .`
- **Format Command**: `ruff format .`

## Key Directories

- `src/` - Source code
- `tests/` - Test files
- `api/` - API routes/endpoints
- `models/` - Pydantic models
- `services/` - Business logic

## Code Style

- Type hints required for all functions
- Use `dataclass` or Pydantic models for data structures
- Prefer early returns, avoid deep nesting
- Log levels: DEBUG, INFO, WARNING, ERROR

## Git Conventions

- **Branch naming**: `{type}/{description}` (e.g., `feat/user-auth`, `fix/login-bug`)
- **Commit format**: Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`)
- **PR titles**: Same as commit format

## Critical Rules

### Error Handling
- Always use proper exceptions
- Log errors with appropriate level
- Return meaningful error messages in APIs

### API Design
- Use Pydantic models for request/response validation
- Follow REST conventions
- Include proper HTTP status codes

### Async
- Use `async/await` for I/O operations
- Prefer `httpx` for async HTTP clients

## Testing

- Use `pytest` with fixtures
- Write tests for all public functions
- Use `pytest-asyncio` for async tests
- Aim for 80%+ coverage

## Common Commands

```bash
# Development
python -m uvicorn app.main:app --reload  # Start dev server
pytest                                    # Run tests
pytest --cov=src                          # Run with coverage
ruff check .                              # Lint
ruff format .                             # Format
```

## Skill Activation

Before implementing ANY task, check if relevant skills apply:

- Writing tests → `python-testing` skill
- Building APIs → `fastapi-patterns` skill
- Debugging issues → `systematic-debugging` skill
- Database operations → `sqlalchemy-patterns` skill
