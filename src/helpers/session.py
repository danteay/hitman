"""
Session helpers
"""

from src.commons.jwt import decode
from src.commons.errors import InvalidSessionToken
from src.commons.mongo import get_connection


def validate(event):
    """
    Validate session token from Lambda event data
    :param event: Lambda data
    :return: decoded session
    """

    if "X-Jwt-Session" not in event["headers"]:
        raise InvalidSessionToken()

    token = event["headers"]["X-Jwt-Session"]

    db_client = get_connection()
    user = db_client.users.find_one({"session": token})

    if not user:
        raise InvalidSessionToken()

    return decode(token)
