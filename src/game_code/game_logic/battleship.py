"""
A basic command line multiplayer battleship implementation.
"""
import game_utils as utils
from ship import Ship, SHIP_TYPES
from src.game_code.game_logic.game_utils import print_board

IS_PLAYER_TURN = True
ALL_SHIPS_PLACED = False

SHIP_STATUS = [True for _ in range(len(SHIP_TYPES))]
PLAYER_GAME_BOARD = utils.init_board(player=True)
OPPONENT_GAME_BOARD = utils.init_board(player=False)

utils.print_board(PLAYER_GAME_BOARD)
utils.print_board(OPPONENT_GAME_BOARD)

# What do I need to make this work?
# - Place ships (orientation?)
#test_ship = Ship("Battleship", "S", 0, 0, utils.BOARD_DIMENSIONS)
#print(test_ship)
#utils.place_ship(PLAYER_GAME_BOARD, test_ship)
#utils.print_board(PLAYER_GAME_BOARD)

# - Guess ship locations
# - Validate guesses
test_guess = (0,0)
utils.guess(PLAYER_GAME_BOARD, test_guess)
utils.print_board(PLAYER_GAME_BOARD)

# - Keep track of ship status (floating/sunk) -> ship_status[] w/ booleans
# while true in ship_status?

# - Turn based -> is_player_turn : boolean
# -- change boolean at the end of the turn
# -- will need some sort of indicator of turn status for players
def setup_board():
    for ship_type, ship_length in SHIP_TYPES.items():
        print(f'Place your {ship_type} of length {ship_length}.')
        print("Select Orientation N/S/E/W: ", end='')
        orientation = str(input)
        print("Bow X Coordinate: ", end='')
        x = int(input())
        print("Bow Y Coordinate: ", end='')
        y = int(input())
        new_ship = Ship(ship_type, orientation, x, y)
        utils.place_ship(PLAYER_GAME_BOARD, new_ship)

def player_turn():
    """ Player turn logic """
    if IS_PLAYER_TURN:
        print("It is your turn...", end='\n')
        print_board()

        if ALL_SHIPS_PLACED:
            try:
                # guess
                print("Enter guess X coordinate: ")
                x = int(input())
                print("Enter guess Y coordinate: ")
                y = int(input())
                x_y = (x,y)
                utils.guess(OPPONENT_GAME_BOARD, x_y)
            except ValueError:
                print("Invalid input...")
                return False

        else:
            # place ships
            setup_board()

    else:
        print("It is the opponents turn...", end='n')
        # receive updates from server about opponent guesses...
        # Display board status
