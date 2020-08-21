"""
Users service actions
"""

import bcrypt

from bson.objectid import ObjectId

from src.commons.mongo import get_connection
from src.commons.logger import LOGGER as logger
from src.commons.errors import UserConflict, UnauthorizedUser
from src.commons.jwt import sign, decode
from src.config import CONFIG


class UsersService:
    """
    User service actions
    """

    @staticmethod
    def list():
        """
        List all users according session
        :return: List of users
        """

        db = get_connection()

        all_users = db.users.find()

        def pars_list(user):
            user["_id"] = str(user["_id"])
            return user

        return list(map(pars_list, all_users))

    @staticmethod
    def register(name, email, password, user_type):
        """
        Register new user in database
        :param name: User name
        :param email: Unique user email
        :param password: Password
        :param user_type: Type of user to be registered (MANAGER | HITMAN)
        :return: New inserted user id
        """

        db = get_connection()

        hash_pass = bcrypt.hashpw(
            password.encode("utf-8"),
            CONFIG["salt"].encode("utf-8")
        ).decode("utf-8")

        user = {
            "name": name,
            "email": email,
            "password": hash_pass,
            "type": user_type
        }

        logger.field("user", user).debug("new user")

        try:
            user = db.users.insert_one(user)

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

        db = get_connection()

        user = db.users.find_one({"email": email})

        if not user:
            raise UnauthorizedUser()

        verify_pass = bcrypt.checkpw(
            password.encode("utf-8"),
            user["password"].encode("utf-8")
        )

        if not verify_pass:
            raise UnauthorizedUser()

        jwt_data = {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "user_type": user["user_type"] if "user_type" in user else None
        }

        token = sign(jwt_data).decode("utf-8")

        db.users.update(
            {"_id": ObjectId(user["_id"])},
            {"$set": {"session": token}}
        )

        return {"token": token}

    @staticmethod
    def logout(token):
        """
        Terminate active session
        :param token: session token
        """

        db = get_connection()

        user_jwt = decode(token)

        user = db.users.find_one({"_id": ObjectId(user_jwt["_id"])})

        if not user:
            raise UnauthorizedUser("not found user")

        if user["session"] != token:
            raise UnauthorizedUser("wrong session")

        db.users.update(
            {"_id": ObjectId(user_jwt["_id"])},
            {"$set": {"session": None}}
        )
