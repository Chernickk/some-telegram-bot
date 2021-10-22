import datetime
from base64 import urlsafe_b64encode, urlsafe_b64decode


def encode_payload(payload: str) -> str:
    """Encode payload with URL-safe base64url."""
    payload = str(payload)
    bytes_payload: bytes = urlsafe_b64encode(payload.encode())
    str_payload = bytes_payload.decode()
    return str_payload.replace("=", "")


def create_payload(uuid,
                   from_datetime: datetime.datetime,
                   to_datetime: datetime.datetime):
    if from_datetime.date() != to_datetime.date():
        raise ValueError('Datetimes should have same date!')
    return f'{uuid} {from_datetime.strftime("%d.%m.%Y,%H.%M.%S")},{to_datetime.strftime("%H.%M.%S")}'


def create_url(payload, bot_username):
    # payload = create_payload(uuid, from_datetime, to_datetime)
    payload = encode_payload(payload)

    if len(payload) > 64:
        raise ValueError('Encoded payload must be up to 64 characters long.')

    return f"https://t.me/{bot_username}?start={payload}"
