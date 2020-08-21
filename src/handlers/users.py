"""
Register User handler
"""

import json

from src.commons.logger import init_logger, LOGGER as logger
from src.commons.http import response, error_response
from src.services.users import UsersService


def register(event, context):
    """
    Lambda handler for register user
    :param event: Lambda event data
    :param context: Lambda context
    :return: Api gateway response
    """

    init_logger()

    try:
        body = json.loads(event["body"])
        user = UsersService.register(**body)

        return response(200, body=user)
    except Exception as err:
        logger.error("registration error", err)
        return error_response(err)


def list_users(event, context):
    """
    Lambda handler to get all users
    :param event: Lambda event data
    :param context: Lambda context
    :return: Api gateway response
    """

    init_logger()

    try:
        return response(200, body=UsersService.list())
    except Exception as err:
        logger.error("list error", err)
        return error_response(err)


def login(event, context):
    """
    Lambda handler to login users
    :param event: Lambda event data
    :param context: Lambda context
    :return: Api gateway response
    """

    init_logger()

    try:
        body = json.loads(event["body"])
        return response(200, body=UsersService.login(**body))
    except Exception as err:
        logger.error("list error", err)
        return error_response(err)


def logout(event, context):
    """
    Lambda handler to delete active session from a suer
    :param event: Lambda event data
    :param context: Lambda context
    :return: Api gateway response
    """

    init_logger()

    try:
        print(event)
        return response(200)
    except Exception as err:
        logger.error("list error", err)
        return error_response(err)
