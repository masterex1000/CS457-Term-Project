# A flexable lobby system that manages active games, allows
# users to connect/disconnect, and routes messages between connections

import uuid
import secrets

from src.game_code.game_logic.player import Player


class GameLobby:
    def __init__(self, name: str, max_players: int):
        self.lobby_name = name
        self.lobby_id = str(uuid.uuid4())
        self.lobby_ticket = secrets.token_hex(16)
        self.max_players = max_players
        self.current_players = 0
        self.players = [] # List of user connections to route messages to

    """ This section defines the lobby messages """
    def _connect_user(self, event) -> bool:
        try:
            user = event.to_dict()
            user_id = user[1]
            username = user[2]
            user_token = user[3]
            new_user = Player(user_id, username, user_token)
            self.players.append(new_user)
        except (IndexError, ValueError):
            return False
        return True

    def _disconnect_user(self, event):
        try:
            user = event.to_dict()
            user_id = user[1]
            self.players.pop(self.players.index(user_id))
        except (IndexError, ValueError):
            return False
        return True

    def _start_game(self, event):
        pass

    def _end_game(self, event):
        pass

    def _has_open_slot(self):
        return self.current_players < self.max_players

    def _handle_chat_messages(self, event):
        pass

    def _parse_event_type(self, event):
        self._log_event(event)
        return event.action

    def _on_event(self, event):
        """Takes an event and processes it's state, propagating any messages to connected clients if necessary"""
        event_type = self._parse_event_type(event)

        # Lobby Events:
        # connect user to the lobby
        #  -> updates the players array with the request information
        if event_type == "connect_user":
            self._connect_user(event)

        # disconnects user from the lobby
        #  -> updates players array and lobby state
        if event_type == "disconnect_user":
            self._disconnect_user(event)

        # chat message
        #  -> send a message to the output stream of both clients
        if event_type == "chat_message":
            self._handle_chat_messages(event)

        # start game
        #  -> create and start a game
        if event_type == "start_game":
            self._start_game(event)

        # end game
        # -> end the game
        if event_type == "end_game":
            self._end_game(event)

    def _log_event(self, event):
        pass

