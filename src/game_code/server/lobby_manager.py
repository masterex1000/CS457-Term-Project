# The lobby managment system, allows users to connect and disconnect from/to and search for lobbys

from typing import List
from lobby import GameLobby

lobbies : List[GameLobby] = []

def getLobbyList(hasOpenSlot = False) -> List[GameLobby]:
    return [lobby for lobby in lobbies if (not hasOpenSlot or lobby.hasOpenSlot())]