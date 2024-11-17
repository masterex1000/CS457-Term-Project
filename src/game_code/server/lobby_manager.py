# The lobby management system, allows users to connect and disconnect from/to and search for lobbies

from typing import List
from server.lobby import GameLobby

# Not a class because it would just end up needing to be a singleton

lobbies: List[GameLobby] = []

def get_lobby_list(self, has_open_slot=False) -> List[GameLobby]:
    """ Client requests a list of lobbies, then lobby manager responds with a list of available lobbies """
    return [lobby for lobby in self.lobbies if (not has_open_slot or lobby.has_open_slot())]

def join_lobby(self, event):
    """ Lobby manager handles client request to join available lobby. Responds with a lobby_ticket """
    try:
        unpacked_event = event.to_dict()
        join_lobby_id = unpacked_event["lobby_id"]
        user_id = unpacked_event["user_id"]
        user_token = unpacked_event["user_token"]

    except:
        lobby_ticket = -1

    return lobby_ticket

def createLobby(name: str, maxPlayers: int) -> GameLobby:
    lobby = GameLobby(name, maxPlayers)
    lobbies.append(lobby)
    
    return lobby

def getLobbyFromId(id: str) -> GameLobby:
    for lobby in lobbies:
        if lobby.lobbyId == id:
            return lobby
    return None

def leave_lobby(self, event):

    pass


def chat_message(self, event):
    pass


def start_game(self, event):
    pass

def _log_event(self, event):
    pass