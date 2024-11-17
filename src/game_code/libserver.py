
import sys
import selectors
import json
import io
import struct
from message import Message

from server import lobby_manager
from connection import Connection
from server.lobby import GameLobby

class ServerConnection(Connection):
    def __init__(self, selector, sock, addr):
        Connection.__init__(self, selector, sock, addr)

    def on_message(self, message):
        action = message.get("action")

        message_module, message_action = action.split('.')

        if message_module == "lobby":
            self.handle_lobby_message(message_action, message)
        if message_module == "game":
            self.handle_game_message(message_action, message)
        else:  # Old handling, keeping for debug reasons
            if action == "message":
                msg = message.get("value")
                content = {"result": msg}
            else:
                content = {"result": f'Error: invalid action "{action}".'}

            self.send_message(content)

    def handle_lobby_message(self, message_action, message):
        # Handling/Routing lobby messages here since we don't know exactly where they'll go yet
        
        if message_action == 'get_lobby_list':
            lobbies = [{'name': lobby.lobby_name,
                        "currentPlayers": lobby.current_players,
                        "maxPlayers": lobby.max_players,
                        "lobbyId": lobby.lobby_id}
                       for lobby in lobby_manager.get_lobby_list()]

            self.send_message({"action": "lobby.lobbyList", "lobbies": lobbies})
            pass
        if message_action == 'createLobby':
            maxPlayers = message.get("maxPlayers")
            
            if maxPlayers < 2:
                self.respond_to_message(message, {"action": "error", "message": "Need at least 2 players in a lobby"})
                return
            
            # Just so we don't have to handle more than 2 players rn
            if maxPlayers > 2:
                self.respond_to_message(message, {"action": "error", "message": "Can't have more than 2 players in a lobby"})
            
            lobby: GameLobby = lobby_manager.createLobby(message.get("name"), message.get("maxPlayers"))
            if lobby.connect_user(self):
                self.respond_to_message(message, {"action": "lobby.joinLobby", "id": lobby.lobbyId})
            else:
                self.respond_to_message(message, {"action": "lobby.leaveLobby", "id": lobby.lobbyId})
            pass
        
        if message_action == 'joinLobby':
            lobby = lobby_manager.getLobbyFromId(message.get("id", None))
            
            if lobby != None:
                lobby.connect_user(self)
            pass
        
        if message_action == 'leaveLobby':
            lobby = lobby_manager.getLobbyFromId(message.get("id", None))
            
            if lobby != None:
                lobby.disconnect_user(self)
            
            self.respond_to_message(message, {"action": "lobby.leaveLobby", "id": message.get("id", None)})
            
        if message_action == 'chatMessage':
            lobby = lobby_manager.getLobbyFromId(message.get("id", None))
            
            if lobby == None:
                return
            
            lobby.handleChatMessage(self, message.get("message", ""))

        if message_action == 'startGame':
            # TODO: implement
            pass

    def handle_game_message(self, message_action: str, message):
        # We'll forward every game message to whatever lobby it is from
        
        lobby = lobby_manager.getLobbyFromId(message.get("lobby_id", None))
        
        if lobby == None:
            return # Ignore this message... Client doesn't know what it is doing

        lobby.onGameMessage(self, message_action, message)