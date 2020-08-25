"""
function helpers for user checkups
"""

from bson.objectid import ObjectId

from src.commons.mongo import get_connection
from src.commons.errors import InvalidUser, UnauthorizedUser
from src.config import CONFIG


def is_active(user_id):
    """
    Check if a current user is active or not
    :param user_id: User ID
    :return: bool
    """

    user = get_user(user_id)
    return user["active"]


def is_master(user_id):
    """
    Validate if the user id correspond to the master admin user
    :param user_id: User id
    :return: bool
    """

    return user_id == CONFIG["master_user"]


def ensure_manager(user_id, manager_id):
    """
    Ensure that the manager of the user match with the given data
    :param user_id: Current user to ensure his manager
    :param manager_id: Manager ID to be checked
    :return: bool
    """

    user = get_user(user_id)

    if "manager_id" not in user:
        return False

    return str(user["manager_id"]) == manager_id


def get_user(user_id):
    """
    Get a single user record
    :param user_id: User ID
    :return: user record
    """

    db_client = get_connection()

    user = db_client.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        raise InvalidUser()

    return user


def only_managers_and_master(session):
    """
    Validate that the accessing user is a manager or the master user
    :param session: Session info
    """

    if session["user_type"] != "manager":
        raise UnauthorizedUser("resource is not able for this user")

    if not is_master(session["id"]):
        raise UnauthorizedUser("resource is not able for this user")
