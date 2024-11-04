
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

        message_module, message_action = action.split('.')

        if message_module == "lobby":
            self.handle_lobby_message(message_action, message)
        else:  # Old handling, keeping for debug reasons
            if action == "message":
                msg = message.get("value")
                content = {"result": msg}
            else:
                content = {"result": f'Error: invalid action "{action}".'}

            self.send_message(content)

    def handle_lobby_message(self, message_action, message):
        if message_action == 'get_lobby_list':
            lobbies = [{'name': lobby.lobby_name,
                        "currentPlayers": lobby.current_players,
                        "maxPlayers": lobby.max_players,
                        "lobbyId": lobby.lobby_id}
                       for lobby in lobby_manager.get_lobby_list()]

            self.send_message({"action": "lobby.lobbyList", "lobbies": lobbies})
            pass
        if message_action == 'joinLobby':
            pass
        if message_action == 'leaveLobby':
            pass
        if message_action == 'chatMessage':
            pass
        if message_action == 'startGame':
            pass
