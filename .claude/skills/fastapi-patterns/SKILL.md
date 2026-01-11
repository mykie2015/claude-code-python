---
name: fastapi-patterns
description: FastAPI patterns for building REST APIs. Use when creating endpoints, validation, or error handling.
---

# FastAPI Patterns

## When to Use
- Creating API endpoints
- Request/response validation
- Error handling
- Dependency injection

## Basic Endpoint

```python
# api/users.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from src.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 10,
    service: UserService = Depends(get_user_service)
) -> List[UserResponse]:
    """List all users with pagination."""
    users = service.list_users(skip=skip, limit=limit)
    return [UserResponse.model_validate(u) for u in users]

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    """Get user by ID."""
    user = service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(data: UserCreate, service: UserService = Depends(get_user_service)):
    """Create new user."""
    user = service.create(data.model_dump())
    return UserResponse.model_validate(user)
```

## Error Handling

```python
# api/errors.py
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
```

## Dependencies

```python
# api/dependencies.py
from typing import Annotated
from src.db.session import get_db_session
from src.services.user_service import UserService

async def get_db():
    async with get_db_session() as session:
        yield session

async def get_user_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserService:
    return UserService(repo=UserRepository(session=db))
```

## Validation

```python
from pydantic import field_validator, model_validator
from datetime import date

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    birth_date: Optional[date] = None
    
    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v
```

## Best Practices
- Use Pydantic models for all validation
- Include docstrings on endpoints
- Use proper HTTP status codes
- Version your API: `/api/v1/`
