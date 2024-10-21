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
         - Each ship can be positioned either North, South, East, or West.
         - Every ship has an (x,y) coordinate for the ship bow (front)
    """
    # state vars
    _type = ""
    _length = 0
    _orientation = '$'
    _bow_position = (0,0)
    _floating = False
    
    # parameterized ctor
    def __init__(self, ship_type, orientation, bow_pos_x, bow_pos_y, board_dim=10):
        # ctor needs to:
        # set ship type, orientation, and bow_position (front of the ship)
        # assert invariants
        assert ship_type in SHIP_TYPES
        assert orientation in ('N','n','S','s','E','e','W','w')
        assert bow_pos_x < board_dim
        assert bow_pos_y < board_dim

        self.type = ship_type
        self.length = SHIP_TYPES[ship_type] # ship length is the value, type is the key
        self.orientation = orientation.lower()
        self.bow_position = (bow_pos_x, bow_pos_y)

        if orientation == 'n':
            for i in range(self.length):
                if self.bow_position[1] - i < 0:
                    print("Invalid ship placement")
                    exit(-1)

        elif orientation == 'e':
            for i in range(self.length):
                if self.bow_position[0] + i >= board_dim:
                    print("Invalid ship placement")

        elif orientation == 's':
            for i in range(self.length):
                if self.bow_position[1] + i >= board_dim:
                    print("Invalid ship placement")

        elif orientation == 'w':
            for i in range(self.length):
                if self.bow_position[0] - i < board_dim:
                    print("Invalid ship placement")


    def __repr__(self):
        """ repr is used for printing objects """
        return f"Ship: {self.type}\nLength: {self.length}\nOrientation: {self.orientation}\nBow Position: {self.bow_position}\n"
