import hashlib
import uuid

from Exceptions import RoomAuthError
from consts import pepper
from db import (
    add_room,
    add_player,
    room_find_one,
    player_find_one,
    add_player_to_room
)


class Room:
    def __init__(self, room_name: str, _uuid: str, room_password: str = ""):
        self._id = None
        self.room_name = room_name
        self.uuid = _uuid
        self.room_password = room_password
        room = room_find_one({'uuid': self.uuid})
        if not room:
            raise RoomAuthError("uuid not Found!")
        if hashlib.md5((pepper + room['salt'] + self.room_password).encode()).hexdigest() == room['password']:
            self._id = room['_id']
        else:
            raise RoomAuthError("Wrong Password")

    # def create_room(self):
    #     self._id = add_room(self.room_name, self.room_password, self.uuid)


class Player:
    def __init__(self, nickname: str, username: str, password: str, create_user: bool = False):
        self.nickname = nickname
        self.username = username
        self.password = password
        # self._id = add_player(nickname, username, password)
        if create_user:
            self._id = add_player(nickname, username, password)['_id']
        else:
            player = player_find_one({'username': self.username})
            if not player:
                raise RoomAuthError("Username not Found!")
            if hashlib.md5((pepper + player['salt'] + self.password).encode()).hexdigest() == player['password']:
                self._id = player['_id']
            else:
                raise RoomAuthError("Wrong Password")

    def create_room(self, room_name: str, password: str) -> dict:
        """

        :param room_name: name of the room
        :param password: password of the room in plain text
        :return:
        """
        _uuid = str(uuid.uuid4())
        room_info = add_room(room_name, password, _uuid, self.username)
        self.join_room(Room(room_name, _uuid, password))
        return room_info

    def join_room(self, room: Room) -> dict:
        """

        :param room:
        :return:
        """
        return add_player_to_room(self.username, room.uuid)
