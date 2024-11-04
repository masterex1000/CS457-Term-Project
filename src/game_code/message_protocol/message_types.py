""" This file contains definitions of the various message types that the lobby will be sending """
from event import Event
from message import Message

class ConnectUserRequest(Event, Message):
    """ User connection request """
    def __init__(self, lobby_id, user_id):
        self.lobby_id=lobby_id
        self.user_id=user_id

    @property
    def action(self):
        return "connect_user"
    def to_dict(self):
        return self.action

class ConnectUserResponse(Event, Message):
    """ User connection request """

    def __init__(self, lobby_id, user_id):
        self.lobby_id = lobby_id
        self.user_id = user_id

    @property
    def action(self):
        return "connect_user"

    def to_dict(self):
        return { "action": self.action }

class DisconnectUser(Event, Message):
    """ User disconnect request """
    def __init__(self, lobby_id, lobby_ticket, user_id):
        self.lobby_id=lobby_id
        self.lobby_ticket=lobby_ticket
        self.user_id=user_id

    @property
    def action(self):
        return "disconnect_user"
    def to_dict(self):
        return { "action": self.action }

class LobbyGetListMessage(Event, Message):
    """ Sent by Clients to get info about available lobbies """
    def __init__(self, client_id):
        self.client_id=client_id

    @property
    def action(self):
        return "get_lobby_list"
    def to_dict(self):
        return { "action": self.action }

class LobbyListMessage(Event, Message):

    def __init__(self, lobby_list):
        self.lobby_list = lobby_list

    @property
    def action(self):
        return "lobby_list"
    def to_dict(self):
        return { "action": self.action, "list": self.lobby_list }
