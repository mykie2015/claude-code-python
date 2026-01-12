<claude-memory>
# Project Memory: claude-code-python (Auth MVP)

> Last updated: 2026-01-12
> Use this to avoid re-scanning the codebase on each session.

---

## 1. Core Architecture

```
src/
├── api/
│   ├── auth.py          # MAIN: Contains endpoints + Pydantic models + business logic
│   └── login_page.html  # Standalone HTML login page (no framework)
├── models/              # Empty placeholder - models are in auth.py
├── services/            # Empty placeholder - logic is in auth.py
└── __init__.py

tests/
├── test_auth.py         # 430 lines - comprehensive API tests
├── test_login_page.py   # Playwright UI tests
└── test_login_happy_flow.py  # Manual Playwright test
```

**Key Relationship:** `src/api/auth.py` is the monolith - it contains:
- All Pydantic models (LoginRequest, MFAVerifyRequest, TokenResponse, etc.)
- Helper functions (create_access_token, verify_password, get_password_hash)
- Both endpoints (`/auth/login`, `/auth/mfa/verify`)
- Mock user database (in-memory dict)

**Empty Directories:** `models/` and `services/` exist but are unused. Future refactor could split `auth.py`.

---

## 2. Tech Stack & Constraints

**Language:** Python 3.11+

**Key Dependencies:**
| Package | Purpose |
|---------|---------|
| `fastapi>=0.109.0` | Web framework |
| `uvicorn>=0.27.0` | ASGI server |
| `pydantic>=2.5.0` | Validation |
| `python-jose[cryptography]>=3.3.0` | JWT handling |
| `passlib[bcrypt]>=1.7.4` | Password hashing |
| `pytest>=8.0.0` | Testing |
| `pytest-asyncio>=0.23.0` | Async testing |
| `ruff>=0.3.0` | Linting/formatting |

**Linting Rules:**
- Line length: 100 characters
- Ruff rules: `E`, `F`, `I` (isort), `UP` (pyupgrade), `ARG` (flake8-unused-arguments)
- **Strict mode** - no ignores configured

**House Rules (from CLAUDE.md):**
- Type hints required for ALL functions
- Use `dataclass` or Pydantic models for data structures
- Prefer early returns, avoid deep nesting
- Log levels: DEBUG, INFO, WARNING, ERROR
- Use `async/await` for I/O operations

**Git Conventions:**
- Branch naming: `{type}/{description}` (e.g., `feat/user-auth`, `fix/login-bug`)
- Commit format: Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`)

---

## 3. Active Work

**Current Branch:** `feature/auth-mvp` (in worktree at `.worktrees/auth-mvp/`)

**Recent Commits:**
| Hash | Message |
|------|---------|
| `d07e2d3` | feat: add JWT authentication API with login and MFA endpoints |
| `278c5cb` | Initial commit: Python project setup with Claude Code configuration |

**What's Implemented:**
- `POST /auth/login` - Returns MFA challenge or access token
- `POST /auth/mfa/verify` - OTP verification (accepts "123456" for demo)
- JWT token creation with configurable expiry
- Password hashing with bcrypt
- 2 mock users for testing

**In Progress (from plan):**
- Registration endpoint (`POST /auth/register`)
- Refresh token endpoint (`POST /auth/refresh`)
- Logout endpoint (`POST /auth/logout`)
- Environment configuration (`src/config.py`)
- Modernized login page UI

---

## 4. Workflow Gotchas

### Running Tests
```bash
pytest                    # All tests
pytest --cov=src          # With coverage report
pytest tests/test_auth.py # Specific file
```

### Linting & Formatting
```bash
ruff check .              # Lint all
ruff format .             # Format all
```

### Dev Server
```bash
# NOTE: No app.main module exists yet!
# uvicorn command in CLAUDE.md won't work as-is
# Quick fix: python -m uvicorn src.api.auth:router --reload
```

### Environment Variables
- `.env` file required (currently missing)
- `SECRET_KEY` must be set (currently hardcoded - security risk)
- Format: `SECRET_KEY=your-32-char-secret-key`

### Missing Pieces
- No `app.main` module - can't use standard `uvicorn app.main:app`
- No `.env` file - secrets are hardcoded
- Empty `models/` and `services/` directories

---

## 5. Test Users (for manual testing)

| Email | Password | MFA Enabled | OTP |
|-------|----------|-------------|-----|
| `test@example.com` | `password123` | Yes | `123456` |
| `user@example.com` | `securepass` | No | - |

---

## 6. Quick Reference

**File to modify for new endpoints:** `src/api/auth.py`
**File to modify for tests:** `tests/test_auth.py`
**File to modify for UI:** `src/api/login_page.html`

**CLAUDE.md location:** `.claude/CLAUDE.md` (project instructions)

---

## 7. Next Steps (from design doc)

The auth MVP enhancement plan includes:
1. Create `src/config.py` with Pydantic-Settings
2. Add `POST /auth/register` endpoint
3. Add `POST /auth/refresh` endpoint
4. Add `POST /auth/logout` endpoint
5. Modernize login page UI (refined minimalism)
6. All new endpoints require tests

Plan saved at: `docs/plans/2026-01-12-auth-mvp-implementation.md`
</claude-memory>
