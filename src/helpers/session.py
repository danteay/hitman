"""
Session helpers
"""

from src.commons.jwt import decode
from src.commons.errors import InvalidSessionToken, UnauthorizedUser
from src.commons.mongo import get_connection
from src.helpers.users import is_master


def validate(event):
    """
    Validate session token from Lambda event data
    :param event: Lambda data
    :return: Decoded session
    """

    if "X-Jwt-Session" not in event["headers"]:
        raise InvalidSessionToken()

    token = event["headers"]["X-Jwt-Session"]

    db_client = get_connection()
    user = db_client.users.find_one({"session": token})

    if not user:
        raise InvalidSessionToken()

    return decode(token)


def only_managers_and_master(event):
    """
    Validate that the accessing user is a manager or the master user
    :param event: Lambda event data
    :return: Decoded session
    """

    session = validate(event)

    if session["user_type"] != "manager" and not is_master(session["id"]):
        raise UnauthorizedUser("resource is not able for this user")

    return session
