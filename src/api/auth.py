"""Authentication API endpoints."""

from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, HTTPException, Request, status
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr, field_validator

from src.config import settings

# Use settings from config
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
MFA_TOKEN_EXPIRE_MINUTES = settings.MFA_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

router = APIRouter(prefix="/auth", tags=["authentication"])


# ============ Pydantic Models ============


class LoginRequest(BaseModel):
    """Login request with email, password, and country code."""

    email: EmailStr
    password: str
    country_code: str

    @field_validator("country_code")
    @classmethod
    def validate_country_code(cls, v: str) -> str:
        if len(v) != 2:
            raise ValueError("Country code must be 2 characters (ISO 3166-1 alpha-2)")
        return v.upper()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class MFAVerifyRequest(BaseModel):
    """MFA verification request with OTP code."""

    email: EmailStr
    otp_code: str

    @field_validator("otp_code")
    @classmethod
    def validate_otp(cls, v: str) -> str:
        if not v.isdigit() or len(v) != 6:
            raise ValueError("OTP must be 6 digits")
        return v


class TokenResponse(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class MFAResponse(BaseModel):
    """MFA challenge response."""

    message: str
    mfa_required: bool = True
    temp_token: str | None = None


class ErrorResponse(BaseModel):
    """Error response model."""

    detail: str


class RegisterRequest(BaseModel):
    """Registration request."""

    email: EmailStr
    password: str
    country_code: str

    @field_validator("country_code")
    @classmethod
    def validate_country_code(cls, v: str) -> str:
        if len(v) != 2:
            raise ValueError("Country code must be 2 characters")
        return v.upper()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        return v


class RegisterResponse(BaseModel):
    """Registration response."""

    id: int
    email: str
    message: str = "Registration successful"


class RefreshRequest(BaseModel):
    """Refresh token request."""

    refresh_token: str


class RefreshResponse(BaseModel):
    """Refresh token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class LogoutRequest(BaseModel):
    """Logout request."""

    refresh_token: str


class LogoutResponse(BaseModel):
    """Logout response."""

    message: str = "Successfully logged out"


# ============ Helper Functions ============


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_mfa_temp_token(data: dict) -> str:
    """Create a temporary token for MFA verification flow."""
    expires_delta = timedelta(minutes=MFA_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"mfa_pending": True})
    return create_access_token(to_encode, expires_delta)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


# ============ Mock User Database ============

# In production, this would be replaced with actual database calls
MOCK_USERS: dict[str, dict] = {
    "test@example.com": {
        "id": 1,
        "email": "test@example.com",
        "password_hash": get_password_hash("password123"),
        "mfa_enabled": True,
        "mfa_secret": "ABCDEFGHIJKLMNOP",  # In production, use proper TOTP secret
    },
    "user@example.com": {
        "id": 2,
        "email": "user@example.com",
        "password_hash": get_password_hash("securepass"),
        "mfa_enabled": False,
        "mfa_secret": None,
    },
}

# User storage for registration (in-memory for MVP)
REGISTERED_USERS: dict[str, dict] = {}
USER_ID_COUNTER = {"next_id": 3}  # Start after existing mock users

# Refresh token storage (in-memory for MVP)
REVOKED_REFRESH_TOKENS: set[str] = set()


def create_refresh_token(data: dict) -> str:
    """Create a JWT refresh token with longer expiry."""
    to_encode = data.copy()
    to_encode.update({"token_type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


# ============ Endpoints ============


@router.post(
    "/login",
    response_model=MFAResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
        404: {"model": ErrorResponse, "description": "User not found"},
    },
)
async def login(request: LoginRequest) -> MFAResponse:
    """
    Authenticate user with email and password.

    Returns a temporary token if MFA is required, or access token if not.
    """
    user = MOCK_USERS.get(request.email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not verify_password(request.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Check if MFA is required
    if user["mfa_enabled"]:
        temp_token = create_mfa_temp_token({"sub": user["email"], "user_id": user["id"]})
        return MFAResponse(
            message="MFA verification required",
            mfa_required=True,
            temp_token=temp_token,
        )

    # Generate access token for non-MFA users
    access_token = create_access_token({"sub": user["email"], "user_id": user["id"]})

    return MFAResponse(
        message="Login successful",
        mfa_required=False,
        temp_token=access_token,
    )


@router.post(
    "/mfa/verify",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid or expired token"},
        401: {"model": ErrorResponse, "description": "Invalid OTP code"},
    },
)
async def verify_mfa(
    request: MFAVerifyRequest,
    http_request: Request,
) -> TokenResponse:
    """
    Verify MFA OTP code and return access token.

    Requires a valid temporary token from the login endpoint in the Authorization header.
    """
    # Extract temp token from Authorization header
    auth_header = http_request.headers.get("Authorization")
    temp_token = None
    if auth_header and auth_header.startswith("Bearer "):
        temp_token = auth_header[7:]

    if not temp_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing or invalid Authorization header",
        )

    # Simplified MFA verification for demonstration
    # In production, use pyotp or similar library:
    # import pyotp
    # totp = pyotp.TOTP(user['mfa_secret'])
    # if not totp.verify(request.otp_code):
    #     raise HTTPException(...)

    # For demo purposes, accept "123456" as valid OTP
    if request.otp_code != "123456":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid OTP code",
        )

    # Verify temp token and extract user info
    try:
        payload = jwt.decode(temp_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub") or ""
        user_id: int = payload.get("user_id") or 0
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired session. Please login again.",
        )

    user = MOCK_USERS.get(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )

    # Generate final access token
    access_token = create_access_token({"sub": email, "user_id": user_id})

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Email already registered or invalid input"},
    },
)
async def register(request: RegisterRequest) -> RegisterResponse:
    """Register a new user."""
    # Check if email already exists
    if request.email in MOCK_USERS or request.email in REGISTERED_USERS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create new user
    user_id = USER_ID_COUNTER["next_id"]
    USER_ID_COUNTER["next_id"] += 1

    REGISTERED_USERS[request.email] = {
        "id": user_id,
        "email": request.email,
        "password_hash": get_password_hash(request.password),
        "mfa_enabled": False,
        "mfa_secret": None,
    }

    return RegisterResponse(
        id=user_id,
        email=request.email,
    )


@router.post(
    "/refresh",
    response_model=RefreshResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or expired refresh token"},
    },
)
async def refresh_token(request: RefreshRequest) -> RefreshResponse:
    """Refresh access token using refresh token."""
    # Check if token is revoked
    if request.refresh_token in REVOKED_REFRESH_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
        )

    # Decode and validate refresh token
    payload = decode_token(request.refresh_token)

    if payload.get("token_type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    # Create new access token
    access_token = create_access_token(
        {"sub": payload.get("sub"), "user_id": payload.get("user_id")}
    )

    return RefreshResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post(
    "/logout",
    response_model=LogoutResponse,
    status_code=status.HTTP_200_OK,
    responses={},
)
async def logout(request: LogoutRequest) -> LogoutResponse:
    """Logout and revoke refresh token."""
    # Add to revoked tokens (in-memory, grows unbounded in MVP)
    REVOKED_REFRESH_TOKENS.add(request.refresh_token)

    return LogoutResponse()
