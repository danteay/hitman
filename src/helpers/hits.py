"""
Common hit helper functions
"""

from src.commons.errors import InvalidHit


def get_hit(mongo, filters=None, qry_fields=None):
    """
    Return hit information
    :param mongo: Database Connection
    :param filters: Query filters
    :param qry_fields: fields to return on response
    :return: hit info
    """

    if not filters:
        filters = {}

    if not qry_fields:
        hit = mongo.hits.find_one(filters)
    else:
        hit = mongo.hits.find_one(filters, qry_fields)

    if not hit:
        raise InvalidHit()

    return hit


def get_all_hits(mongo, filters=None):
    """
    Return all hits according provided filters
    :param mongo: Database connection
    :param filters: data filters
    :return: list of hits
    """

    if not filters:
        filters = {}

    return mongo.hits.find(filters)
