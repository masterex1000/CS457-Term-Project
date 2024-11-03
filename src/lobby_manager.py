# The lobby managment system, allows users to connect and disconnect from/to and search for lobbys

from typing import List
from lobby import GameLobby

lobbies : List[GameLobby] = []

def getLobbyList(hasOpenSlot = False) -> List[GameLobby]:
    return [lobby for lobby in lobbies if (not hasOpenSlot or lobby.hasOpenSlot())]

def createLobby(name: str, maxPlayers: int) -> GameLobby:
    lobby = GameLobby(name, maxPlayers)
    lobbies.append(lobby)
    
    return lobby

def getLobbyFromId(id: str) -> GameLobby:
    for lobby in lobbies:
        if lobby.lobbyId == id:
            return lobby
    return None