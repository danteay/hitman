"""
Mongo connection
"""

import pymongo

from src.config import CONFIG


def get_connection():
    """
    Build a new Mongo connection client
    :return: Mongo database
    """

    client = pymongo.MongoClient(CONFIG["database"])
    return client.hitmen
