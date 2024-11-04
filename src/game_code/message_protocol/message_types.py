""" This file contains definitions of the various message types that the lobby will be sending """
from event import Event
from message import Message

class ConnectUserRequest(Event, Message):
    """ User connection request """
    def __init__(self, user_id, username="Anonymous User"):
        self.user_id=user_id
        self.username=username

    @property
    def action(self):
        return "connect_user"
    def to_dict(self):
        return dict(action=self.action)
# end class def

class ConnectUserResponse(Event, Message):
    """ User connection response """
    def __init__(self,  user_id, username, status="Connection Failed!!!"):
        self.user_id = user_id
        self.username = username
        self.status = status

    @property
    def action(self):
        return "connect_user"
    def to_dict(self):
        return dict(action=self.action, username=self.username, status=self.status)
# end class def

class DisconnectUserRequest(Event, Message):
    """ User disconnect request """
    def __init__(self, lobby_id, lobby_ticket, user_id):
        self.lobby_id=lobby_id
        self.lobby_ticket=lobby_ticket
        self.user_id=user_id

    @property
    def action(self):
        return "disconnect_user"
    def to_dict(self):
        return dict(action=self.action, lobby_id=self.lobby_id, lobby_ticket=self.lobby_ticket, user_id=self.user_id)
# end class def

class DisconnectUserResponse(Event, Message):
    """ User disconnect response """
    def __init__(self, lobby_id, lobby_ticket, user_id, success=False):
        self.lobby_id=lobby_id
        self.lobby_ticket=lobby_ticket
        self.user_id=user_id
        self.success=success

    @property
    def action(self):
        return "disconnect_user"
    def to_dict(self):
        return dict(action=self.action, success=self.success)
# end class def

class LobbyListRequest(Event, Message):
    """ Sent by Clients to get info about available lobbies """
    def __init__(self, client_id):
        self.client_id=client_id

    @property
    def action(self):
        return "get_lobby_list"
    def to_dict(self):
        return dict(action=self.action, client_id=self.client_id)
# end class def

class LobbyListResponse(Event, Message):
    """ Response sent by Server to Clients with available lobbies """
    def __init__(self, lobby_list, success=False):
        self.lobby_list=lobby_list
        self.success=success

    @property
    def action(self):
        return "lobby_list"
    def to_dict(self):
        return {
            "action": self.action,
            "success":self.success,
            "list": self.lobby_list
        }
# end class def

class JoinLobbyRequest(Event, Message):
    """ Client request to join a specified lobby"""
    def __init__(self, lobby_id, show_username=False):
        self.lobby_id = lobby_id
        self.show_username=show_username

    @property
    def action(self):
        return "join_lobby"
    def to_dict(self):
        d = {
            "action": self.action,
            "lobby_id": self.lobby_id,
            "show_username": self.show_username
        }
        return d
# end class def

class JoinLobbyResponse(Event, Message):
    """ Client request to join a specified lobby"""
    def __init__(self, lobby_id, user_id, success=False):
        self.lobby_id = lobby_id
        self.user_id = user_id
        self.success=success

    @property
    def action(self):
        return "join_lobby"
    def to_dict(self):
        return { "action": self.action, "lobby_id": self.lobby_id, "success": self.success }
# end class def