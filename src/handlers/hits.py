"""
Lambda handlers for Hit actions
"""

import json

import src.helpers.session as session_helper

from src.commons.logger import init_logger, LOGGER as logger
from src.commons.http import response, error_response
from src.commons.mongo import get_connection
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
        session = session_helper.only_managers_and_master(get_connection(), event)
        body = json.loads(event["body"])

        return response(200, body=HitsService.create(session["id"], **body))
    except Exception as err:
        logger.error("registration error", err)
        return error_response(err)


def list_hits(event, context):
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


def fetch_hit(event, context):
    """
    Lambda handler fetch hit info
    :param event: Lambda event data
    :param context: Lambda context
    :return: Api gateway response
    """

    try:
        session = session_helper.validate(event)
        hit_id = event["pathParameters"]["hit_id"]

        return response(200, body=HitsService.fetch_hit(session, hit_id))
    except Exception as err:
        logger.error("registration error", err)
        return error_response(err)


def assign_hit(event, context):
    """
    Lambda handler to assign hitmen to hits
    :param event: Lambda event data
    :param context: Lambda context
    :return: Api gateway response
    """

    try:
        session = session_helper.only_managers_and_master(get_connection(), event)
        hit_id = event["pathParameters"]["hit_id"]
        body = json.loads(event["body"])

        return response(
            200, body=HitsService.assign_hit(session, hit_id, body["user_id"])
        )
    except Exception as err:
        logger.error("registration error", err)
        return error_response(err)
