"""
Init user base on database from the first start
"""

from src.services.users import UsersService
from src.commons.logger import LOGGER as logger

BASE_USERS = [
    {
        "name": "Veda",
        "email": "veda@gmail.com",
        "password": "12345678",
        "description": "Celestial Being Founder"
    },
    {
        "name": "Sumeragui Le Noriega",
        "email": "Sumeragui@gmail.com",
        "password": "12345678",
        "description": "Gundam Manager"
    },
    {
        "name": "Christina Sierra",
        "email": "christina@gmail.com",
        "password": "12345678",
        "description": "Gundam Manager"
    },
    {
        "name": "Feldt Grace",
        "email": "feldt@gmail.com",
        "password": "12345678",
        "description": "Gundam Manager"
    },
    {
        "name": "Setsuna F. Seiei",
        "email": "setsuna@gmail.com",
        "password": "12345678",
        "description": "Gundam Master"
    },
    {
        "name": "Tieria Erde",
        "email": "tieria@gmail.com",
        "password": "12345678",
        "description": "Gundam Master"
    },
    {
        "name": "Lockon Stratos",
        "email": "lockon@gmail.com",
        "password": "12345678",
        "description": "Gundam Master"
    },
    {
        "name": "Allelujah Haptism",
        "email": "allelujah@gmail.com",
        "password": "12345678",
        "description": "Gundam Master"
    },
    {
        "name": "Nena Trinity",
        "email": "nena@gmail.com",
        "password": "12345678",
        "description": "Gundam Master"
    }
]


def register(user):
    user_id = UsersService.register(**user)["_id"]
    user["_id"] = str(user_id)
    return user


def main():
    users = list(map(register, BASE_USERS))

    logger.fields({"base_users": users}).debug("inserted base users")

    UsersService.assign_manager(users[4]["_id"], users[1]["_id"])
    UsersService.assign_manager(users[5]["_id"], users[1]["_id"])
    UsersService.assign_manager(users[6]["_id"], users[1]["_id"])
    UsersService.assign_manager(users[7]["_id"], users[2]["_id"])
    UsersService.assign_manager(users[8]["_id"], users[2]["_id"])
    UsersService.assign_manager(users[5]["_id"], users[3]["_id"])

    db = UsersService.DB

    db.users.create_index("email", unique=True)
    db.users.create_index("session")

    db.hits.create_index("user_id")

    pass


if __name__ == '__main__':
    main()
