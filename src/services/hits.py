"""
Hit service actions
"""

from bson.objectid import ObjectId

from src.commons.mongo import get_connection
from src.commons.logger import LOGGER as logger
from src.commons.errors import InvalidHit, InactiveUser, UnauthorizedUser, InvalidUser
from src.helpers.users import is_active, ensure_manager, get_user, is_master


class HitsService:

    @staticmethod
    def list(session):
        """
        Return all available hits according the user
        :param session: Current user session
        :return: list of hits
        """

        filters = {}

        if not is_master(session["id"]):
            user = get_user(session["id"])
            user_list = [user["_id"]]

            if "subordinates" in user:
                user_list = user_list + user["subordinates"]
                user_list.append(None)

            filters = {"user_id": {"$in": user_list}}

        logger.fields({"filters": filters}).debug("filtering hits")

        db_client = get_connection()
        all_hits = db_client.hits.find(filters)

        return list(all_hits)

    @staticmethod
    def create(manager_id, target, description, user_id=None):
        """
        Register new hit target
        :param manager_id: Current manager that is creating the hit
        :param target: Target name
        :param description: Brief description of the hit
        :param user_id: User id of the assigned hitman
        """

        manager = get_user(manager_id)

        if not manager:
            raise InvalidUser("invalid manager id")

        if user_id is not None:
            if manager_id == user_id:
                raise InvalidHit("self assigned hit")

            if not is_master(manager_id) and not ensure_manager(user_id, manager_id):
                raise UnauthorizedUser("manager can't assign hits to this user")

            if not is_active(user_id):
                raise InactiveUser("hitman is inactive")

        data_hit = {
            "target": target,
            "description": description,
            "user_id": ObjectId(user_id) if user_id is not None else None,
            "status:": "assigned" if user_id is not None else "created",
            "creator_id": ObjectId(manager_id)
        }

        db_client = get_connection()
        hit = db_client.hits.insert_one(data_hit)

        return {"id": hit.inserted_id}
