# A flexable lobby system that manages active games, allows
# users to connect/disconnect, and routes messages between connections

import uuid

class GameLobby:
    def __init__(self, name: str, maxPlayers: int):
        self.lobbyName = name
        self.lobbyId = str(uuid.uuid4())
        self.maxPlayers = maxPlayers
        self.currentPlayers = 0
        self.players = [] # List of user connections to route messages to
    
    # Takes an event and processes it's state, propagating any messages to connected clients if necessary
    def process_event(self):
        pass

    def connect_user(self) -> bool:
        return False

    def disconnect_user(self):
        pass
    
    def hasOpenSlot(self):
        return self.currentPlayers < self.maxPlayers