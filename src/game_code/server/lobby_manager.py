# The lobby management system, allows users to connect and disconnect from/to and search for lobbies

from typing import List
from lobby import GameLobby

lobbies : List[GameLobby] = []

def get_lobby_list(has_open_slot = False) -> List[GameLobby]:
    return [lobby for lobby in lobbies if (not has_open_slot or lobby.has_open_slot())]