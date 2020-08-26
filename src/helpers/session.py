"""
Session helpers
"""

from src.commons.jwt import decode
from src.commons.errors import InvalidSessionToken, UnauthorizedUser
from src.commons.mongo import get_connection
from src.helpers.users import is_master, get_user


def validate(event):
    """
    Validate session token from Lambda event data
    :param event: Lambda data
    :return: Decoded session
    """

    if "X-Jwt-Session" not in event["headers"]:
        raise InvalidSessionToken()

    token = event["headers"]["X-Jwt-Session"]

    user = get_user(get_connection(), {"session": token})

    if not user:
        raise InvalidSessionToken()

    if not user["active"]:
        raise UnauthorizedUser()

    return decode(token)


def only_managers_and_master(mongo, event):
    """
    Validate that the accessing user is a manager or the master user
    :param mongo: database connection
    :param event: Lambda event data
    :return: Decoded session
    """

    session = validate(event)

    if session["user_type"] != "manager" and not is_master(mongo, session["id"]):
        raise UnauthorizedUser("resource is not able for this user")

    return session
