""" 
 This file defines ship types and sizes, a ship class, and some helper functions. 
"""

SHIP_TYPES = {
    "Carrier" : 5,
    "Battleship" : 4,
    "Cruiser" : 3,
    "Submarine" : 3,
    "Destroyer" : 2
}

class Ship:
    """  
        Ships have the following characteristics:
         - There are several ship types each of a fixed length.
         - Each ship can be positioned either horizontally or vertically.
         - Every ship has a x,y coordinate for the ship bow (front)
    """
    # state vars
    _type = ""
    _length = 0
    _orientation = 'H'
    _bow_position = (0,0)
    _floating = True
    
    # parameterized ctor
    def __init__(self, ship_type, orientation, bow_pos_x, bow_pos_y, board_dim=10):
        # ctor needs to:
        # set ship type, orientation, and bow_position (front of the ship)
        # assert invarients
        assert ship_type in SHIP_TYPES
        assert orientation in ('H','h','V','v')
        assert bow_pos_x < board_dim
        assert bow_pos_y < board_dim

        self.type = ship_type
        self.length = SHIP_TYPES[ship_type] # ship lenth is the value, type is the key
        self.orientation = orientation
        self.bow_position = (bow_pos_x, bow_pos_y)

    def __repr__(self):
        """ repr is used for printing objects """
        return f"Ship: {self.type}\nLength: {self.length}\nOrientation: {self.orientation}\nBow Position: {self.bow_position}\n"
