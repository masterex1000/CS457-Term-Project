# A flexable lobby system that manages active games, allows
# users to connect/disconnect, and routes messages between connections

import uuid

class GameLobby:
    def __init__(self, name: str, max_players: int):
        self.lobby_name = name
        self.lobby_id = str(uuid.uuid4())
        self.max_players = max_players
        self.current_players = 0
        self.players = [] # List of user connections to route messages to

    """ This section defines the """
    def _connect_user(self, event) -> bool:
        return False

    def _disconnect_user(self, event):
        pass

    def _start_game(self, event):
        pass

    def _has_open_slot(self):
        return self.current_players < self.max_players

    def _get_lobby(self, event):
        pass

    def _join_lobby(self, event):
        pass

    def _leave_lobby(self, event):
        pass

    def _chat_message(self, event):
        pass

    def _parse_event_type(self, event):
        return event.action

    def _on_event(self, event):
        """Takes an event and processes it's state, propagating any messages to connected clients if necessary"""

        event_type = self._parse_event_type(event)

        # Events:
        if event_type == "connect_user":
            self._connect_user(event)

        if event_type == "disconnect_user":
            self._disconnect_user(event)

        #   get lobby list
        #       -> returns to sender a list of available lobbies
        if event_type == "get_lobby":
            self._get_lobby(event)

        #   join lobby
        #       -> join a lobby update lobby state, generate token
        if event_type == "join_lobby":
            self._join_lobby(event)

        #   leave lobby
        #       -> leave a lobby using lobby token to authenticate user
        if event_type == "leave_lobby":
            self._leave_lobby(event)

        #   chat message
        #       -> send a message to the output stream of both clients
        if event_type == "chat_message":
            self._chat_message(event)

        #   start game
        #       -> create and start a game
        if event_type == "start_game":
            self._start_game(event)

