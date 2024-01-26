import hashlib
import random
import string
import uuid

from consts import pepper
from db import (
    add_room,
    get_room_salt,
    add_player,
    room_find_all,
    room_find_one
)


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


class Room:
    def __init__(self, room_name: str, _uuid: str, room_password: str = ""):
        self._id = None
        self.room_name = room_name
        self.uuid = _uuid
        self.room_password = room_password

    def authenticate(self) -> bool:
        room = room_find_one({'uuid': self.uuid})
        if not room:
            return False
        if hashlib.md5((pepper + room['salt'] + self.room_password).encode()).hexdigest() == room['password']:
            self._id = room['_id']
            return True
        else:
            return False

    def create_room(self):
        self._id = add_room(self.room_name, self.room_password, self.uuid)


class Player:
    def __init__(self, nickname: str, username: str, password: str):
        self.nickname = nickname
        self.username = username
        self.password = password
        self.uuid = str(uuid.uuid4())
        self._id = add_player(nickname, username, password, self.uuid)

    def create_room(self, room: Room) -> dict:
        """

        :param room: room
        :param player: player
        :return:
        """
        # check if room name already exists
        # add to db
        # return {name, password, _id}
        pass

    def join_room(self, room: Room) -> dict:
        """

        :param room:
        :return:
        """
        # check if room name exists
        # add player to db
        #
        pass
