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
    
    # Takes an event and processes it's state, propagating any messages to connected clients if necessary
    def process_event(self, event):

        type = self.get_event_type(event)

        # Events:
        #   get lobby list
        #       -> returns to sender a list of available lobbies
        if type == "get_lobby":
            print()
            self.handle_get_lobby(event)

        #   join lobby
        #       -> join a lobby update lobby state, generate token
        if type == "join_lobby":
            print()
            self.handle_join_lobby(event)

        #   leave lobby
        #       -> leave a lobby using lobby token to authenticate user
        if type == "leave_lobby":
            print()
            self.handle_leave_lobby(event)

        #   chat message
        #       -> send a message to the output stream of both clients
        if type == "chat_message":
            print()
            self.handle_chat_message(event)

        #   start game
        #       -> create and start a game
        if type == "start_game":
            print()

        if type == "disconnect_user":
            print()
            self.disconnect_user(event)

        pass

    def connect_user(self, event) -> bool:
        return False

    def disconnect_user(self, event):
        pass
    
    def has_open_slot(self):
        return self.current_players < self.max_players

    def handle_get_lobby(self, event):
        pass

    def handle_join_lobby(self, event):
        pass

    def handle_leave_lobby(self, event):
        pass

    def handle_chat_message(self, event):
        pass

    def get_event_type(self, event):
        pass