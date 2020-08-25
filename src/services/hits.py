"""
Hit service actions
"""

from bson.objectid import ObjectId

from src.commons.mongo import get_connection
from src.commons.errors import InvalidHit, InactiveUser, UnauthorizedUser
from src.helpers.users import is_active, ensure_manager, only_managers_and_master


class Hits:
    @staticmethod
    def create(session, target, hitman_id):
        """
        Register new hit target
        :param session: Current user session object
        :param target: Target name
        :param hitman_id: User id of the assigned hitman
        """

        only_managers_and_master(session)

        if session["user_type"] == "manager" and not ensure_manager(
            hitman_id, session["id"]
        ):
            raise UnauthorizedUser("resource is not able for this user")

        if session["id"] == hitman_id:
            raise InvalidHit("self assigned hit")

        if not is_active(hitman_id):
            raise InactiveUser("hitman is inactive")

        data_hit = {"target": target, "user_id": ObjectId(hitman_id)}

        db_client = get_connection()

        hit = db_client.users.insert_one(data_hit)

        return {"id": str(hit.inserted_id)}
