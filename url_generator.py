import datetime
from base64 import urlsafe_b64encode, urlsafe_b64decode


def encode_payload(payload: str) -> str:
    """Encode payload with URL-safe base64url."""
    payload = str(payload)
    bytes_payload: bytes = urlsafe_b64encode(payload.encode())
    str_payload = bytes_payload.decode()
    return str_payload.replace("=", "")


def create_url(payload, bot_username):
    payload = encode_payload(payload)

    if len(payload) > 64:
        raise ValueError('Encoded payload must be up to 64 characters long.')

    return f"https://t.me/{bot_username}?start={payload}"
