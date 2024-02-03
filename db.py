import hashlib
import os
import random
import string
import time
import uuid

from dotenv import load_dotenv
from pymongo import MongoClient

from consts import (
    pepper,
    salt_length
)

from icecream import ic

load_dotenv()


def generate_db_id():
    timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
    unique_id = uuid.uuid4().hex[:12]  # 12 random characters from a UUID4

    mongodb_id = f"{timestamp:x}{unique_id}"  # Combine timestamp and random characters
    return mongodb_id


class RoomDB(list):
    def find(self, q: dict):
        """
        kinda like db.find
        :param q:
        :return:
        """
        results = []
        for item in self:
            q_match = True
            for k in q:
                try:
                    if q[k] != item[k]:
                        q_match = False
                        break
                except KeyError:
                    q_match = False
                    break
            if q_match:
                results.append(item)
        return results

    def find_one(self, q: dict):
        """
        kinda like db.find_one
        :param q:
        :return:
        """
        for item in self:
            q_match = True
            for k in q:
                try:
                    if q[k] != item[k]:
                        q_match = False
                        break
                except KeyError:
                    q_match = False
                    break
            if q_match:
                # results.append(item)
                return item

    def insert_one(self, q: dict):
        """

        :param q:
        :return:
        """
        if '_id' in q:
            raise ValueError('q should not have an attribute called "_id"')
        if self.find_one({'uuid': q['uuid']}):
            raise ValueError('uuid must be unique')
        res = {'_id': generate_db_id()} | q
        self.append(res)
        return res

    def update_one(self, q: dict, new_q: dict) -> dict:
        """

        :param q: search query
        :param new_q: the new value to set for found items
        :return:
        """
        room = self.find_one(q)
        for key in room:
            if key in new_q:
                room[key] = new_q[key]
        # self[]
        return room


def generate_salt(length: int):
    all_characters = string.ascii_letters + string.digits + string.punctuation
    unique_characters = random.sample(all_characters, length)
    random_string = ''.join(unique_characters)
    return random_string


db_client = MongoClient(
    os.getenv('DB_URI'),
)

db = {
    'card_pack': db_client['cah']['card_pack'],
    'player': db_client['cah']['player'],
    'room': RoomDB([])
}


def get_player_salt(q: dict) -> str:
    """

    :param q: the query to search in the database
    :return: the salt related to the given q (query)
    """
    res = db['player'].find_one(q)
    return res['salt']


def get_card_packs() -> [str]:
    """
    read card packs from db
    :return:
    """
    return list(db['card_pack'].find())


def add_player(nickname: str, username: str, password: str) -> dict:
    """

    :param nickname:
    :param username:
    :param password:
    :return: _id of player (str)
    """
    salt = generate_salt(salt_length)
    q = {
        'nickname': nickname,
        'username': username,
        'password': hashlib.md5((pepper + salt + password).encode()).hexdigest(),
        'salt': salt,
        'time': int(time.time()),
    }
    _id = db['player'].insert_one(q)
    q['_id'] = _id
    return q


def player_find_all(q: dict) -> list:
    """

    :param q:
    :return:
    """
    return list(db['player'].find(q))


def player_find_one(q: dict) -> dict:
    """

    :param q:
    :return:
    """
    return db['player'].find_one(q)


def get_room_salt(q: dict) -> str:
    """

    :param q: the query to search in the database
    :return: the salt related to the given q (query)
    """
    res = db['room'].find_one(q)
    return res['salt']


def add_room(nickname: str, password: str, uuid: str, creator: str) -> dict:
    """

    :param nickname: name of the room
    :param password: password in plain text
    :param uuid: the only unique identifier for rooms (other than _id)
    :param creator: username of the creator
    :return: _id of room (str)
    """
    if not db['player'].find_one({'username': creator}):
        raise ValueError('username does not exist')
    salt = generate_salt(salt_length)
    q = {
        "nickname": nickname,
        "uuid": uuid,
        "password": hashlib.md5((pepper + salt + password).encode()).hexdigest(),
        "salt": salt,
        "creator": creator,
        "players": [],
        "time": int(time.time())
    }

    res = db['room'].insert_one(q)
    return res


def add_player_to_room(username: str, room_uuid: str) -> dict:
    """

    :param username:
    :param room_uuid:
    :return:
    """
    room = db['room'].find_one({'uuid': room_uuid})
    if not room:
        raise ValueError("room does not exist")
    if username in room['players']:
        raise ValueError("username is already in this room")
    if not db['player'].find_one({'username': username}):
        raise ValueError('username does not exist')
    return db['room'].update_one(
        {
            'uuid': room_uuid
        }, {
            'players': room['players'] + [username]
        }
    )


def room_find_all(q: dict) -> list:
    """

    :param q:
    :return:
    """
    return list(db['room'].find(q))


def room_find_one(q: dict) -> dict:
    """

    :param q:
    :return:
    """
    return db['room'].find_one(q)
