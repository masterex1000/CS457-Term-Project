""" This module is for declaring functions for the battleship game """

BOARD_DIMENSIONS = 10
OPPONENT_BOARD_BACKGROUND = "?"
PLAYER_BOARD_BACKGROUND = "~"
SHIP_CHARACTER = "$"
HIT_CHARACTER = "X"
MISS_CHARACTER = "~"

def build_board(background_char):
    """ initialize background of the game, usually for either opponent or player """
    return [[background_char for j in range(BOARD_DIMENSIONS)] for i in range(BOARD_DIMENSIONS)]

def init_board(player=True):
    """ Initialize the game board to default setup, player board if arg is True else Opponent """
    if player:
        board = build_board(PLAYER_BOARD_BACKGROUND)
    else:
        board = build_board(OPPONENT_BOARD_BACKGROUND)
    return board

def print_board(board):
    """This function prints the gameboard passed to it """
    if isinstance(board, list):
        # Asserting invarients: board is list representing NxN board
        x_dim = len(board[0])
        y_dim = len(board)
        assert x_dim == y_dim

        # classic double for loop for ease of comprehension
        for y_position in range(y_dim):
            for x_position in range(x_dim):
                print(board[y_position][x_position], end=" ")

            # these print statements are to exiplicitly ensure we print new lines
            print(end="\n")
        print(end="\n")

def place_ship(board, ship):
    """ This function places a ship on the board using some attributes of each ship """
    # ship are defined by the enum inside ship class battleship, cruiser, etc.
    length = ship.length
    bow_pos = ship.bow_position # bow is the front of a ship
    orientation = ship.orientation # horizontal or vertical
    print(length)
    # starting indexes and assertions for bounds checking
    start_x = bow_pos[0]
    assert start_x + length < BOARD_DIMENSIONS
    start_y = bow_pos[1]
    assert start_y + length < BOARD_DIMENSIONS

    if orientation in ("H", "h"):
        # horizontal orientation, use X coordinate bow_pos[0]
        y_idx = start_y
        print("Horizontal Orientation...")

        for i in range(length):
            x_idx = start_x + i
            board[y_idx][x_idx] = SHIP_CHARACTER

    if orientation in ("V", "v"):
        # vertical orientation, use Y coordinate bow_pos[1]
        x_idx = start_x    
        for i in range(length):
            y_idx = start_y + i
            board[y_idx][x_idx] = SHIP_CHARACTER

    print_board(board)
    return board

def guess(board, x_y):
    """ Guess if a particular coordinate is a ship or not... """
    # tuple values
    x = x_y[0]
    y = x_y[1]

    # invarients
    assert x < len(board)
    assert y < len(board)

    # guess
    loc = board[y][x]
    hit = loc=="$"

    # check
    if hit:
        board[y][x] = HIT_CHARACTER
    else:
        board[y][x] = MISS_CHARACTER

    return board
