""" This file contains definitions of the various message types that the lobby will be sending """
from event import Event
from message import Message

class ConnectUserRequest(Event, Message):
    """ User connection request """
    def __init__(self, user_id, username="Anonymous User", password_hash="ABCD"):
        self.user_id=user_id
        self.username=username
        self.password_hash=password_hash

    @property
    def action(self):
        return "connect_user"
    def to_dict(self):
        return dict(action=self.action, username=self.username, password_hash=self.password_hash)
# end class def

class ConnectUserResponse(Event, Message):
    """ User connection response """
    def __init__(self,  user_id, username, user_token, success=False):
        self.user_id = user_id
        self.username = username
        self.user_token = user_token
        self.success = success

    @property
    def action(self):
        return "connect_user"
    def to_dict(self):
        return dict(action=self.action, username=self.username, success=self.success)
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
        return dict(action=self.action, lobby_list=self.lobby_list, success=False)
# end class def

class JoinLobbyRequest(Event, Message):
    """ Client request to join a specified lobby """
    def __init__(self, lobby_id, user_id, user_token):
        self.lobby_id = lobby_id
        self.user_id = user_id
        self.user_token = user_token

    @property
    def action(self):
        return "join_lobby"

    def to_dict(self):
        return dict(action=self.action, lobby_id=self.lobby_id, user_id=self.user_id, user_token=self.user_token)
# end class def

class JoinLobbyResponse(Event, Message):
    """ Server response to client requesting to join a specified lobby """
    def __init__(self, lobby_id, user_id, lobby_token, success=False):
        self.lobby_id = lobby_id
        self.user_id = user_id
        self.success=success

    @property
    def action(self):
        return "join_lobby"

    def to_dict(self):
        return dict(action=self.action, lobby_id=self.lobby_id, success=self.success)
# end class def

class StartGameRequest(Event, Message):
    """ Client signals that it is ready to start the game """
    def __init__(self, user_id, user_token, lobby_id=0, lobby_token=0):
        self.user_id=user_id
        self.user_token=user_token
        self.lobby_id=lobby_id
        self.lobby_token=lobby_token

    @property
    def action(self):
        return "start_game"

    def to_dict(self):
        return dict(
            user_id=self.user_id,
            user_token=self.user_token,
            lobby_id=self.lobby_id,
            lobby_token=self.lobby_token
        )

class StartGameResponse(Event, Message):
    """ Lobby signals the game to start, specifies starting player.py """
    def __init__(self, user_id, lobby_id, lobby_token, success=False):
        self.user_id=user_id
        self.lobby_id=lobby_id
        self.lobby_token=lobby_token
        self.success=success

    @property
    def action(self):
        return "start_game"

    def to_dict(self):
        return dict(
            action=self.action,
            user_id=self.user_id,
            lobby_id=self.lobby_id,
            lobby_token=self.lobby_token,
            success=self.success
        )


class ChatMessageRequest(Event, Message):
    def __init__(self, user_id, user_token, lobby_id, lobby_token, message, checksum):
        self.user_id=user_id
        self.user_token=user_token
        self.lobby_id=lobby_id
        self.lobby_token=lobby_token
        self.message=message
        self.checksum=checksum

    @property
    def action(self):
        return "chat_message"

    def to_dict(self):
        return dict(
            user_id=self.user_id,
            user_token=self.user_token,
            lobby_id=self.lobby_id,
            lobby_token=self.lobby_token,
            message=self.message,
            checksum=self.checksum
        )