"""
Register User handler
"""

import json

import src.helpers.session as session_helper

from src.commons.errors import UnauthorizedUser
from src.commons.logger import init_logger, LOGGER as logger
from src.commons.http import response, error_response
from src.helpers.users import is_master
from src.services.users import UsersService

init_logger()


def register(event, context):
    """
    Lambda handler for register user
    :param event: Lambda event data
    :param context: Lambda context
    :return: Api gateway response
    """

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

    try:
        session = session_helper.validate(event)
        return response(200, body=UsersService.list(session))
    except Exception as err:
        logger.error("list error", err)
        return error_response(err)


def fetch_user(event, context):
    """
    Lambda handler to fetch user info
    :param event: Lambda event data
    :param context: Lambda context
    :return: Api gateway response
    """

    try:
        session = session_helper.validate(event)
        user_id = event["pathParameters"]["user_id"]

        return response(200, body=UsersService.fetch(session, user_id))
    except Exception as err:
        logger.error("fetch user error", err)
        return error_response(err)


def login(event, context):
    """
    Lambda handler to login users
    :param event: Lambda event data
    :param context: Lambda context
    :return: Api gateway response
    """

    try:
        body = json.loads(event["body"])
        return response(200, body=UsersService.login(**body))
    except Exception as err:
        logger.error("login error", err)
        return error_response(err)


def logout(event, context):
    """
    Lambda handler to delete active session from a suer
    :param event: Lambda event data
    :param context: Lambda context
    :return: Api gateway response
    """

    token = event["headers"]["X-Jwt-Session"]

    try:
        return response(200, body=UsersService.logout(token))
    except Exception as err:
        logger.error("logout error", err)
        return error_response(err)


def assign_manager(event, context):
    """
    Lambda handler to assign manager to a user
    :param event: Lambda event data
    :param context: Lambda context
    :return: Api gateway response
    """

    try:
        session = session_helper.validate(event)

        if not is_master(session["id"]):
            raise UnauthorizedUser()

        user_id = event["pathParameters"]["user_id"]

        body = json.loads(event["body"])

        return response(
            200, body=UsersService.assign_manager(user_id, body["manager_id"])
        )
    except Exception as err:
        logger.error("assign manager error", err)
        return error_response(err)
