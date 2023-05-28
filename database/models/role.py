from enum import Enum


class Roles(str, Enum):
    admin = "admin"
    user = "user"
    advanced_user = "advanced_user"

