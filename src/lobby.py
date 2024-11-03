# A flexable lobby system that manages active games, allows
# users to connect/disconnect, and routes messages between connections

import os
import sys
from typing import List
import uuid

sys.path.append(os.path.abspath('../'))
from connection import Connection

class GameLobby:
    def __init__(self, name: str, maxPlayers: int):
        self.lobbyName = name
        self.lobbyId = str(uuid.uuid4())
        self.maxPlayers = maxPlayers
        self.currentPlayers = 0
        self.players: List[Connection] = [] # List of user connections to route messages to
    
    # Takes an event and processes it's state, propagating any messages to connected clients if necessary
    def process_event(self):
        pass

    def connect_user(self, connection: Connection) -> bool:
        if not self.hasOpenSlot():
            return False
        
        self.currentPlayers = self.currentPlayers + 1
        self.players.append(connection)
        
        self.update_lobby_state()

    def disconnect_user(self, connection):
        for i, player in enumerate(self.players):
            if player == connection:
                self.players.pop(i)
                break
        
        self.update_lobby_state()
    
    def update_lobby_state(self):
        state = self.getLobbyStateMessage()
        
        for conn in self.players:
            conn.send_message(state)
    
    def getLobbyStateMessage(self) -> dict:
        return {
            'action': 'lobby.updateLobbyState',
            'name': self.name,
            'id': self.lobbyId,
            'maxPlayers': self.maxPlayers,
            'currentPlayers': self.currentPlayers,
        }
    
    def hasOpenSlot(self):
        return self.currentPlayers < self.maxPlayers
    
    def handleChatMessage(self, srcConnection: Connection, message: str):
        print(f"Lobby [{self.lobbyId}] : Chat from {srcConnection.addr} : '{message}")
        
        reply = {"action": "lobby.chatMessage", message: message, "id": self.lobbyId}
        
        for conn in self.players:
            conn.send_message(reply)