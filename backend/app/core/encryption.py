from __future__ import annotations

"""Fernet-based symmetric encryption for storing API keys at rest."""

from cryptography.fernet import Fernet, InvalidToken

from app.core.config import get_settings


def _get_fernet() -> Fernet:
    """Return a ``Fernet`` instance initialised with the configured key."""
    settings = get_settings()
    return Fernet(settings.ENCRYPTION_KEY.encode())


def encrypt_value(plaintext: str) -> str:
    """Encrypt *plaintext* and return the ciphertext as a UTF-8 string.

    The returned string is safe to store directly in a database column.
    """
    return _get_fernet().encrypt(plaintext.encode()).decode()


def decrypt_value(ciphertext: str) -> str:
    """Decrypt *ciphertext* and return the original plaintext.

    Raises ``cryptography.fernet.InvalidToken`` if the ciphertext is
    invalid or was encrypted with a different key.
    """
    return _get_fernet().decrypt(ciphertext.encode()).decode()


__all__ = ["encrypt_value", "decrypt_value", "InvalidToken"]
