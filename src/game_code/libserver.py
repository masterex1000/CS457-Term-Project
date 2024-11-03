
import sys
import selectors
import json
import io
import struct
from message import Message
from server import lobby_manager
from connection import Connection


class ServerConnection(Connection):
    def __init__(self, selector, sock, addr):
        Connection.__init__(self, selector, sock, addr)

    def on_message(self, message):
        action = message.get("action")

        messageModule, messageAction = action.split('.')

        if messageModule == "lobby":
            self.handle_lobby_message(messageAction, message)
        else:  # Old handling, keeping for debug reasons
            if action == "message":
                msg = message.get("value")
                content = {"result": msg}
            else:
                content = {"result": f'Error: invalid action "{action}".'}

            self.send_message(content)

    def handle_lobby_message(self, messageAction, message):
        if messageAction == 'get_lobby_list':
            lobbies = [{'name': lobby.lobbyName,
                        "currentPlayers": lobby.currentPlayers,
                        "maxPlayers": lobby.maxPlayers,
                        "lobbyId": lobby.lobbyId}
                       for lobby in lobby_manager.get_lobby_list()]

            self.send_message({"action": "lobby.lobbyList", "lobbies": lobbies})
            pass
        if messageAction == 'joinLobby':
            pass
        if messageAction == 'leaveLobby':
            pass
        if messageAction == 'chatMessage':
            pass
        if messageAction == 'startGame':
            pass
