"""
Authorizer handler for session verification
"""

from bson.objectid import ObjectId

from src.commons.mongo import get_connection
from src.commons.logger import LOGGER as logger
from src.commons.jwt import decode


def verify_token(event, context):
    """
    Authenticate user
    :param event: Lambda event data
    :param context: Lambda context
    """

    token = event.get("authorizationToken")

    try:
        user = decode(token)

        db = get_connection()

        user = db.users.find_one({"_id": ObjectId(user["id"])})

        if user and user["session"] and user["session"] == token:
            return user

        raise Exception("invalid token")
    except Exception as error:
        logger.error("authorization error", error)
        raise Exception("unauthorized")



