"""
JWT common implementations
"""

import jwt

from src.config import CONFIG


def sign(user_data):
    """
    Create a new signature session token for a specific user
    :param user_data: JSON user information to be signed
    :return: signed token
    """

    conf = CONFIG["jwt"]

    token = jwt.encode(user_data, conf["secret"], algorithm=conf["algorithm"])

    return token


def decode(token):
    """
    Decode user token information
    :param token: Signed token
    :return: user JSON information
    """

    conf = CONFIG["jwt"]

    user = jwt.decode(token, conf["secret"], algorithms=conf["algorithm"])

    return user
