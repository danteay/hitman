"""Http lambda utils"""

import json
import http.client

from src.commons.errors import HandlerError
from src.commons.logger import LOGGER as logger


def response(code, body=None, error=None):
    """Http lambda response formatting
    :param code: (int) Http response code
    :param body: (dict) Response json body
    :param error: (Exception|dict|str) Possible error on response body
    :return: (dict)
    """

    if not body:
        body = {}

    if error is not None:
        if isinstance(error, HandlerError):
            body["errors"] = error.get_message()
        else:
            body["errors"] = get_error_from_code(code)
            body["message"] = str(error).replace("\n", "")

    logger.field("res", body)

    if "errors" in body and body["errors"] is not None:
        logger.error("handled request", error=body["errors"])
    else:
        logger.info("handled request")

    return {"statusCode": code, "body": json.dumps(body)}


def get_error_from_code(code):
    """
    Transform http status code into a standard error message
    :param code: HTTP status code
    """
    error = http.client.responses[code]
    error = error.lower().replace(" ", "-")
    return error


def error_response(error):
    """
    Identify the error type an respond with the proper error
    :param error: Handled error
    :returns: Api gateway response format
    """

    if isinstance(error, HandlerError):
        return response(code=error.get_code(), error=error)

    return response(code=500, error=error)
