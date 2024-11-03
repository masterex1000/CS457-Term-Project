
import sys
import selectors
import json
import io
import struct
from message import Message
import lobby_manager
from connection import Connection
from lobby import GameLobby

class ServerConnection(Connection):
    def __init__(self, selector, sock, addr):
        Connection.__init__(self, selector, sock, addr)

    def on_message(self, message):
        action = message.get("action")

        messageModule, messageAction = action.split('.')

        if messageModule == "lobby":
            self.handleLobbyMessage(messageAction, message)
        else:  # Old handling, keeping for debug reasons
            if action == "debug.message":
                msg = message.get("value")
                content = {"result": msg}
            else:
                content = {"result": f'Error: invalid action "{action}".'}

            self.send_message(content)

    def handleLobbyMessage(self, messageAction: str, message:dict):
        if messageAction == 'getLobbyList':
            lobbies = [{'name': lobby.lobbyName,
                        "currentPlayers": lobby.currentPlayers,
                        "maxPlayers": lobby.maxPlayers,
                        "lobbyId": lobby.lobbyId}
                        for lobby in lobby_manager.getLobbyList()]

            self.respond_to_message(message, {"action": "lobby.lobbyList", "lobbies": lobbies})
            pass
        if messageAction == 'joinLobby':
            maxPlayers = message.get("maxPlayers")
            
            if maxPlayers < 2:
                self.respond_to_message(message, {"action": "error", "message": "Need at least 2 players in a lobby"})
                return
            
            lobby: GameLobby = lobby_manager.createLobby(message.get("name"), message.get("maxPlayers"))
            if lobby.connect_user(self):
                self.respond_to_message(message, {"action": "lobby.joinLobby", "id": lobby.lobbyId})
            else:
                self.respond_to_message(message, {"action": "lobby.leaveLobby", "id": lobby.lobbyId})
        
        if messageAction == 'leaveLobby':
            lobby = lobby_manager.getLobbyFromId(message.get("id", None))
            
            if lobby != None:
                lobby.disconnect_user(self)
            
            self.respond_to_message(message, {"action": "lobby.leaveLobby", "id": message.get("id", None)})

            pass
        if messageAction == 'chatMessage':
            lobby = lobby_manager.getLobbyFromId(message.get("id", None))
            
            if lobby == None:
                return
            
            lobby.handleChatMessage(self, message.get("message", ""))
        if messageAction == 'startGame':
            pass
