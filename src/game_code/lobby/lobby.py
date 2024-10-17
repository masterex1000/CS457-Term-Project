# A flexable lobby system that manages active games, allows
# users to connect/disconnect, and routes messages between connections


class GameLobby:
    def __init__(self, name: str, maxPlayers: int):
        self.lobbyName = name
        self.maxPlayers = maxPlayers
        self.currentPlayers = 0
        self.players = [] # List of user connections to route messages to
    
    # Takes an event and processes it's state, propagating any messages to connected clients
    def process_event():
        pass

    def connect_user() -> bool:
        return False

    def disconnect_user():
        pass