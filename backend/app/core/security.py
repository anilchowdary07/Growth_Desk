from __future__ import annotations

"""JWT token management and password hashing utilities."""

from datetime import UTC, datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt
import bcrypt

from app.core.config import get_settings

# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------


def hash_password(password: str) -> str:
    """Return a bcrypt hash of *password*."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Return ``True`` if *plain_password* matches *hashed_password*."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except Exception:
        return False


# ---------------------------------------------------------------------------
# JWT tokens
# ---------------------------------------------------------------------------


def create_access_token(
    user_id: UUID,
    *,
    extra_claims: dict | None = None,
) -> str:
    """Create a short-lived JWT access token for *user_id*."""
    settings = get_settings()
    now = datetime.now(UTC)
    payload = {
        "sub": str(user_id),
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(user_id: UUID) -> str:
    """Create a long-lived JWT refresh token for *user_id*."""
    settings = get_settings()
    now = datetime.now(UTC)
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "iat": now,
        "exp": now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token.

    Raises ``JWTError`` on invalid / expired tokens.
    """
    settings = get_settings()
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])


def verify_access_token(token: str) -> UUID | None:
    """Return the ``user_id`` from a valid access token, or ``None``."""
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            return None
        user_id_str = payload.get("sub")
        if user_id_str is None:
            return None
        return UUID(user_id_str)
    except (JWTError, ValueError):
        return None


def verify_refresh_token(token: str) -> UUID | None:
    """Return the ``user_id`` from a valid refresh token, or ``None``."""
    try:
        payload = decode_token(token)
        if payload.get("type") != "refresh":
            return None
        user_id_str = payload.get("sub")
        if user_id_str is None:
            return None
        return UUID(user_id_str)
    except (JWTError, ValueError):
        return None
