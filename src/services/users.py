"""
Users service actions
"""

import bcrypt

from bson.objectid import ObjectId
from validate_email import validate_email

from src.commons.mongo import get_connection
from src.commons.logger import LOGGER as logger
from src.commons.errors import (
    UserConflict,
    UnauthorizedUser,
    InactiveUser,
    InvalidUser,
    InvalidSessionToken,
    InvalidUserInfo,
)
from src.commons.jwt import sign, decode
from src.helpers.users import is_active, is_master, get_user
from src.config import CONFIG


class UsersService:
    """
    User service actions
    """

    @staticmethod
    def list(session):
        """
        List all users according session
        :param session: Current user session
        :return: List of users
        """

        filters = {}

        if not is_master(session["id"]):
            user = get_user(session["id"])
            user_list = [user["_id"]]

            if "subordinates" in user:
                user_list = user_list + user["subordinates"]

            filters = {"_id": {"$in": user_list}}

        db_client = get_connection()
        all_users = db_client.users.find(filters, {"password": 0})

        return list(all_users)

    @staticmethod
    def fetch(session, user_id):
        """
        Get the information of a single hitman
        :param session: Current user session
        :param user_id: User Id to fetch the info
        :return: User info
        """

        if not is_master(session["id"]):
            user = get_user(session["id"])

            if "subordinates" not in user:
                raise UnauthorizedUser()

            if ObjectId(user_id) not in user["subordinates"]:
                raise UnauthorizedUser()

        db_client = get_connection()
        user = db_client.users.find_one({"_id": ObjectId(user_id)}, {"password": 0})

        if not user:
            raise InvalidUser()

        return user

    @staticmethod
    def register(name, email, password, description=None):
        """
        Register new user in database
        :param name: User name
        :param email: Unique user email
        :param password: Password
        :param description: Hitmen description
        :return: New inserted user id
        """

        if not validate_email(email):
            raise InvalidUserInfo()

        db_client = get_connection()

        hash_pass = bcrypt.hashpw(
            password.encode("utf-8"), CONFIG["salt"].encode("utf-8")
        ).decode("utf-8")

        user = {
            "name": name,
            "email": email,
            "password": hash_pass,
            "active": True,
            "description": description,
        }

        logger.field("user", user).debug("new user")

        try:
            user = db_client.users.insert_one(user)

            return {"id": str(user.inserted_id)}
        except Exception as error:
            logger.error("user registration error", error)
            raise UserConflict(error)

    @staticmethod
    def login(email, password):
        """
        Start new session
        :param email: Unique user email
        :param password: Password
        """

        db_client = get_connection()

        user = db_client.users.find_one({"email": email})

        if not user or not user["active"]:
            raise UnauthorizedUser()

        verify_pass = bcrypt.checkpw(
            password.encode("utf-8"), user["password"].encode("utf-8")
        )

        if not verify_pass:
            raise UnauthorizedUser()

        jwt_data = {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "user_type": user["user_type"] if "user_type" in user else None,
        }

        token = sign(jwt_data).decode("utf-8")

        db_client.users.update(
            {"_id": ObjectId(user["_id"])}, {"$set": {"session": token}}
        )

        return {"token": token}

    @staticmethod
    def logout(token):
        """
        Terminate active session
        :param token: session token
        """

        db_client = get_connection()

        user_id = decode(token)["id"]

        user = db_client.users.find_one({"_id": ObjectId(user_id)})

        if not user:
            raise InvalidUser("not found user")

        if user["session"] != token:
            raise InvalidSessionToken()

        db_client.users.update({"_id": ObjectId(user_id)}, {"$set": {"session": None}})

        return {"message": "session closed"}

    @staticmethod
    def assign_manager(user_id, manager_id):
        """
        Assign a corresponding manager to a hitman
        :param user_id: User ID
        :param manager_id: Manager ID
        """

        if not is_active(user_id):
            raise InactiveUser("hitman is inactive")

        if not is_active(manager_id):
            raise InactiveUser("manager is inactive")

        db_client = get_connection()

        db_client.users.update(
            {"_id": ObjectId(user_id)}, {"$set": {"manager_id": ObjectId(manager_id)}}
        )

        db_client.users.update(
            {"_id": ObjectId(manager_id)},
            {
                "$set": {"user_type": "manager"},
                "$addToSet": {"subordinates": ObjectId(user_id)},
            },
        )

        return {"message": "manager assigned"}

    @staticmethod
    def deactivate(user_id):
        """
        Deactivate a user
        :param user_id:
        """

        db_client = get_connection()
        db_client.users.update({"_id": ObjectId(user_id)}, {"$set": {"active": False}})
        return {"message": "user deactivated"}
