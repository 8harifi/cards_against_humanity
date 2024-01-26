from pymongo import MongoClient
import os
from dotenv import load_dotenv
import hashlib
import string
import random

from consts import (
    pepper,
    salt_length
)

load_dotenv()


def generate_salt(length: int):
    all_characters = string.ascii_letters + string.digits + string.punctuation
    unique_characters = random.sample(all_characters, length)
    random_string = ''.join(unique_characters)
    return random_string


db = MongoClient(
    os.getenv('DB_URI'),
)


def get_player_salt(q: dict) -> str:
    """

    :param q: the query to search in the database
    :return: the salt related to the given q (query)
    """
    res = db['cah']['player'].find_one(q)
    return res['salt']


def get_room_salt(q: dict) -> str:
    """

    :param q: the query to search in the database
    :return: the salt related to the given q (query)
    """
    res = db['cah']['room'].find_one(q)
    return res['salt']


def add_player(nickname: str, username: str, password: str, uuid: str) -> str:
    """

    :param nickname:
    :param username:
    :param password:
    :param uuid:
    :return: _id of player (str)
    """
    salt = generate_salt(salt_length)
    _id = db['cah']['players'].insert_one(
        {
            'nickname': nickname,
            'username': username,
            'password': hashlib.md5((pepper + salt + password).encode()).hexdigest(),
            'salt': salt
        }
    )
    return str(_id)


def add_room(nickname: str, password: str, uuid: str) -> str:
    """

    :param nickname:
    :param password:
    :param uuid:
    :return: _id of room (str)
    """
    salt = generate_salt(salt_length)
    _id = db['cah']['rooms'].insert_one(
        {
            "nickname": nickname,
            "uuid": uuid,
            "password": hashlib.md5((pepper + salt + password).encode()).hexdigest(),
            "salt": salt,
        }
    )
    return str(_id)


def get_card_packs() -> [str]:
    """
    read card packs from db
    :return:
    """
    return list(db['cah']['card_packs'].find())


def room_find_all(q: dict) -> list:
    """

    :param q:
    :return:
    """
    return list(db['cah']['rooms'].find(q))


def room_find_one(q: dict) -> dict:
    """

    :param q:
    :return:
    """
    return db['cah']['rooms'].find_one(q)
