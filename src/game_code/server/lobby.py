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
    def process_event(self):

        # Events:
        #   get lobby list
        #       -> returns to sender a list of available lobbies
        #   join lobby
        #       -> join a lobby update lobby state, generate token
        #   leave lobby
        #       -> leave a lobby using lobby token to authenticate user
        #   chat message
        #       -> send a message to the output stream of both clients
        #   start game
        #       -> create and start a game

        pass

    def connect_user(self) -> bool:
        return False

    def disconnect_user(self):
        pass
    
    def has_open_slot(self):
        return self.currentPlayers < self.max_players