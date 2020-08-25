"""
Lambda handlers for Hit actions
"""

import json

import src.helpers.session as session_helper

from src.commons.logger import init_logger, LOGGER as logger
from src.commons.http import response, error_response
from src.services.hits import HitsService

init_logger()


def create(event, context):
    """
    Lambda handler to create a new hit, the hit can be assigned or not assigned to a hitman
    :param event: Lambda event data
    :param context: Lambda context
    :return: Api gateway response
    """

    try:
        session = session_helper.only_managers_and_master(event)
        body = json.loads(event["body"])

        return response(200, body=HitsService.create(session["id"], **body))
    except Exception as err:
        logger.error("registration error", err)
        return error_response(err)


def list(event, context):
    """
    Lambda handler to list all available hits according user
    :param event: Lambda event data
    :param context: Lambda context
    :return: Api gateway response
    """

    try:
        session = session_helper.validate(event)
        return response(200, body=HitsService.list(session))
    except Exception as err:
        logger.error("registration error", err)
        return error_response(err)
