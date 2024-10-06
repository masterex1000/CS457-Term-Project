"""
A basic command line multiplayer battleship implementation.
"""
import game_utils as utils
from ship import Ship, SHIP_TYPES

IS_PLAYER_TURN = True
SHIP_STATUS = [True for _ in range(len(SHIP_TYPES))]
PLAYER_GAME_BOARD = utils.init_board(player=True)
OPPONENT_GAME_BOARD = utils.init_board(player=False)

utils.print_board(PLAYER_GAME_BOARD)
utils.print_board(OPPONENT_GAME_BOARD)

# What do I need to make this work?
# - Place ships (orientation?)
test_ship = Ship("Battleship", "H", 0, 0, utils.BOARD_DIMENSIONS)
print(test_ship)
utils.place_ship(PLAYER_GAME_BOARD, test_ship)
utils.print_board(PLAYER_GAME_BOARD)

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
def player_turn():
    """ Player turn logic """
    if IS_PLAYER_TURN:
        print("It is your turn...", end='\n')
    else:
        print("It is the opponents turn...", end='n')
# if player_turn:
# print It's your turn...
# else:
#   what should people be able to do if it's not their turn?
# - Display board status
# - print Its the opponents turn...
