"""
A basic command line multiplayer battleship implementation.
"""
import game_utils as utils
from ship import Ship, SHIP_TYPES
from src.game_code.game_logic.game_utils import print_board

class BattleShip:
    def __init__(self):

        self.IS_PLAYER_TURN = True
        self.ALL_SHIPS_PLACED = False

        self.SHIP_STATUS = [True for _ in range(len(SHIP_TYPES))]
        self.PLAYER_GAME_BOARD = utils.init_board(player=True)
        self.OPPONENT_GAME_BOARD = utils.init_board(player=False)


    # - Turn based -> is_player_turn : boolean
    # -- change boolean at the end of the turn
    # -- will need some sort of indicator of turn status for players
    def setup_board(self):
        for ship_type, ship_length in SHIP_TYPES.items():
            print(f'Place your {ship_type} of length {ship_length}.')
            print("Select Orientation N/S/E/W: ", end='')
            orientation = str(input)
            print("Bow X Coordinate: ", end='')
            x = int(input())
            print("Bow Y Coordinate: ", end='')
            y = int(input())
            new_ship = Ship(ship_type, orientation, x, y)
            utils.place_ship(self.PLAYER_GAME_BOARD, new_ship)


    def get_updated_board_state(self):
        """ Requests from the server the updated board state. Generally called at the beginning of the player.py's turn. """
        return NotImplemented

    def player_turn(self):
        """ Player turn logic """
        if self.IS_PLAYER_TURN:
            print("It is your turn...", end='\n')
            print_board()

            if self.ALL_SHIPS_PLACED:
                try:
                    #get_updated_board_state()
                    # guess
                    print("Enter guess X coordinate: ")
                    x = int(input())
                    print("Enter guess Y coordinate: ")
                    y = int(input())
                    x_y = (x,y)
                    utils.guess(self.OPPONENT_GAME_BOARD, x_y)
                except ValueError:
                    print("Invalid input...")
                    return False

            else:
                # place ships
                self.setup_board()

        else:
            print("It is the opponents turn...", end='n')
            # receive updates from server about opponent guesses...
            # Display board status
