"""
Hit service actions
"""

from bson.objectid import ObjectId

from src.commons.mongo import get_connection
from src.commons.logger import LOGGER as logger
from src.commons.errors import (
    InvalidHit,
    InactiveUser,
    UnauthorizedUser,
    InvalidUser,
    BlockedHit,
    WrongHitStatus,
)
from src.helpers.users import is_active, ensure_manager, get_user, is_master
from src.helpers.hits import get_hit


class HitsService:
    """
    User service functions
    """

    DB = get_connection()

    @staticmethod
    def list(session):
        """
        Return all available hits according the user
        :param session: Current user session
        :return: list of hits
        """

        filters = {}

        if not is_master(HitsService.DB, session["id"]):
            user = get_user(HitsService.DB, {"_id": ObjectId(session["id"])})
            user_list = [user["_id"]]

            if "subordinates" in user:
                user_list = user_list + user["subordinates"]
                user_list.append(None)

            filters = {"user_id": {"$in": user_list}}

        logger.fields({"filters": filters}).debug("filtering hits")

        all_hits = HitsService.DB.hits.find(filters)

        return list(all_hits)

    @staticmethod
    def fetch_hit(session, hit_id):
        """
        Fetch hit information according current session
        :param session: current user session
        :param hit_id: Hit id
        :return: hit info
        """

        hit = get_hit(HitsService.DB, {"_id": ObjectId(hit_id)})

        if is_master(HitsService.DB, session["id"]):
            return hit

        user = get_user(HitsService.DB, {"_id": ObjectId(session["id"])})

        if hit["user_id"] == user["_id"] or hit["user_id"] in user["subordinates"]:
            return hit

        raise UnauthorizedUser()

    @staticmethod
    def create(manager_id, target, description, user_id=None):
        """
        Register new hit target
        :param manager_id: Current manager that is creating the hit
        :param target: Target name
        :param description: Brief description of the hit
        :param user_id: User id of the assigned hitman
        """

        logger.fields({"user_id": user_id}).debug("hit user")

        manager = get_user(HitsService.DB, {"_id": ObjectId(manager_id)})

        if not manager:
            raise InvalidUser("invalid manager id")

        if user_id is not None:
            if manager_id == user_id:
                raise InvalidHit("self assigned hit")

            if not is_master(HitsService.DB, manager_id) and not ensure_manager(
                HitsService.DB, user_id, manager_id
            ):
                raise UnauthorizedUser("manager can't assign hits to this user")

            if not is_active(HitsService.DB, user_id):
                raise InactiveUser("hitman is inactive")

        data_hit = {
            "target": target,
            "description": description,
            "user_id": ObjectId(user_id) if user_id is not None else None,
            "status": "assigned" if user_id is not None else "created",
            "creator_id": ObjectId(manager_id),
        }

        hit = HitsService.DB.hits.insert_one(data_hit)

        return {"id": hit.inserted_id}

    @staticmethod
    def assign_hit(session, hit_id, user_id):
        """
        Assign an active hitman to an available hit, also a hit can be reassigned
        by overriding the current assigned hitman
        :param session: Current user session
        :param hit_id: Hit id to assign
        :param user_id: Hitman user id that will be assigned to the hit
        """

        if session["user_type"] == "manager" and not ensure_manager(
            HitsService.DB, user_id, session["id"]
        ):
            raise UnauthorizedUser()

        hit = get_hit(HitsService.DB, {"_id": ObjectId(hit_id)})

        logger.fields({"hit": hit}).debug("current hit")

        if hit["status"] == "failed" or hit["status"] == "closed":
            raise BlockedHit()

        user = get_user(HitsService.DB, {"_id": ObjectId(user_id)})

        if not user["active"]:
            raise InvalidUser("hitman is not active")

        if session["id"] == user_id:
            raise InvalidUser("self assigned hit")

        HitsService.DB.hits.update(
            {"_id": ObjectId(hit_id)},
            {"$set": {"user_id": ObjectId(user_id), "status": "assigned"}},
        )

        return {"message": "hit updated"}

    @staticmethod
    def change_status(session, hit_id, status):
        """
        Change the status of an active hit from assigned to failure or closed
        :param session: current user session
        :param hit_id: Hit ID to update
        :param status: New status of the hit
        """

        if session["user_type"] != "manager":
            raise UnauthorizedUser()

        hit = get_hit(HitsService.DB, {"_id": ObjectId(hit_id)})

        if hit["user_id"] == session["id"]:
            raise UnauthorizedUser("self status change")

        if not ensure_manager(HitsService.DB, hit["user_id"], session["id"]):
            raise UnauthorizedUser("hitman is not subordinate of this user")

        if hit["status"] != "assigned":
            raise WrongHitStatus("current status ia different of 'assigned'")

        if status != "failed" or status != "closed":
            raise WrongHitStatus(f"invalid new status '{status}'")

        HitsService.DB.update({"_id": ObjectId(hit_id)}, {"$set": {"status": status}})

        return {"message": "hit status updated"}
