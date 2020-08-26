"""
function helpers for user checkups
"""

from bson.objectid import ObjectId

from src.commons.errors import InvalidUser


def is_active(mongo, user_id):
    """
    Check if a current user is active or not
    :param mongo: Database connection
    :param user_id: User ID
    :return: bool
    """

    user = get_user(mongo, {"_id": ObjectId(user_id)})
    return user["active"]


def is_master(mongo, user_id):
    """
    Validate if the user id correspond to the master admin user
    :param mongo: Database connection
    :param user_id: User id
    :return: bool
    """

    user = mongo.users.find_one()

    return user and str(user["_id"]) == user_id


def ensure_manager(mongo, user_id, manager_id):
    """
    Ensure that the manager of the user match with the given data
    :param mongo: Database connection
    :param user_id: Current user to ensure his manager
    :param manager_id: Manager ID to be checked
    :return: bool
    """

    user = get_user(mongo, {"_id": ObjectId(user_id)})

    if "manager_id" not in user:
        return False

    return str(user["manager_id"]) == manager_id


def get_user(mongo, filters=None, qry_fields=None):
    """
    Get a single user record
    :param mongo: Database connection
    :param filters: User ID
    :param qry_fields: Fields to return in query
    :return: user record
    """

    if not filters:
        filters = {}

    if not qry_fields:
        user = mongo.users.find_one(filters)
    else:
        user = mongo.users.find_one(filters, qry_fields)

    if not user:
        raise InvalidUser()

    return user


def get_all_users(mongo, filters=None, qry_fields=None):
    """
    Return all available users according filters
    :param mongo: Database Connection
    :param filters: Data filters
    :param qry_fields: Files to include or exclude in response
    :return: list of users
    """

    if not filters:
        filters = {}

    if not qry_fields:
        return mongo.users.find(filters)

    return mongo.users.find(filters, qry_fields)
