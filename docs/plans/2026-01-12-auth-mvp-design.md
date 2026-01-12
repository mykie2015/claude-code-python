# Auth MVP Enhancement Design

**Date:** 2026-01-12

## Overview

Enhance the login prototype with registration, refresh tokens, logout, environment config, and UI modernization.

---

## 1. Registration Endpoint

**Endpoint:** `POST /auth/register`

### Request
```json
{
  "email": "user@example.com",
  "password": "securepass123",
  "country_code": "US"
}
```

### Validation
- Email: valid format, not already registered
- Password: 8+ chars, at least 1 number
- Country: 2-char ISO code

### Data Flow
```
Request → Validate email/password → Hash password → Store user → Return 201 Created
```

### Error Responses
- 400: Invalid input or email already exists
- 422: Validation error

### Storage
- In-memory mock database for MVP (swappable for real DB later)

---

## 2. Login Page UI Modernization

**Aesthetic:** Refined Minimalism

### Design System
- **Typography:** Playfair Display (display) + Source Serif 4 (body)
- **Colors:** Soft cream background, dark charcoal text, muted gold accent
- **Layout:** Centered card, generous padding, subtle shadows

### UI Elements
- Email + password fields with floating labels
- Country dropdown with searchable filter
- Password visibility toggle with icon animation
- "Remember me" checkbox with custom styling
- Loading spinner overlay during API calls
- Error messages in subtle toast notifications
- Responsive design for mobile

### Interactions
- Focus states with gentle border color changes
- Button hover: subtle lift + shadow increase
- Form validation: real-time feedback on blur
- Page load: staggered fade-in for elements

### Technical
- Pure HTML/CSS/JS
- No frameworks

---

## 3. Refresh Token & Logout Endpoints

### `POST /auth/refresh`

**Request:**
```json
{
  "refresh_token": "eyJ..."
}
```

**Response:**
```json
{
  "access_token": "new.jwt.token",
  "token_type": "bearer"
}
```

**Validation:**
- Refresh token not expired (7 days)
- User still exists

**Error:** 401 if refresh token invalid/expired

### `POST /auth/logout`

**Request:**
```json
{
  "refresh_token": "eyJ..."
}
```

**Response:** 200 OK

**Behavior:** Adds token to blocklist

### Token Strategy

| Token Type | Expiry | Storage |
|------------|--------|---------|
| Access | 30 min | Memory |
| Refresh | 7 days | HTTP-only cookie |

### Security
- Rotate-on-use: new refresh token issued with each access token refresh
- Detects token theft (if attacker uses stolen refresh token, legitimate user's next refresh will fail)
- Blocklist: in-memory set of revoked refresh tokens (MVP: in-memory, prod: Redis)

---

## 4. Environment Configuration

### `src/config.py`
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"
```

### `.env` File
```
SECRET_KEY=your-super-secret-key-min-32-chars
```

**Important:** Add `.env` to `.gitignore`

### Fallback
- Development key logged as warning if env not set

---

## Files to Modify/Create

| File | Action |
|------|--------|
| `src/config.py` | Create |
| `src/api/auth.py` | Modify (add register, refresh, logout) |
| `src/api/login_page.html` | Modify (modernize UI) |
| `tests/test_auth.py` | Modify (add tests for new endpoints) |
| `.env.example` | Create |

---

## Test Coverage

- Registration success/failure
- Refresh token success/invalid/expired
- Logout success
- Duplicate email registration
- Password strength validation
