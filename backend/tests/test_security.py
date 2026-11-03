import pytest
from app.core.encryption import decrypt_value, encrypt_value
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_access_token,
    verify_password,
    verify_refresh_token,
)
import uuid


def test_password_hashing():
    pwd = "super-secret-password-123"
    hashed = hash_password(pwd)
    assert hashed != pwd
    assert verify_password(pwd, hashed)
    assert not verify_password("wrong-password", hashed)


def test_jwt_tokens():
    user_id = uuid.uuid4()
    access = create_access_token(user_id)
    assert access is not None
    verified = verify_access_token(access)
    assert verified == user_id

    refresh = create_refresh_token(user_id)
    assert refresh is not None
    verified_ref = verify_refresh_token(refresh)
    assert verified_ref == user_id


def test_fernet_encryption():
    secret_key = "sk-proj-test1234567890abcdef"
    encrypted = encrypt_value(secret_key)
    assert encrypted != secret_key
    decrypted = decrypt_value(encrypted)
    assert decrypted == secret_key

