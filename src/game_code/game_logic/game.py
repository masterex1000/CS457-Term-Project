"""
This file encapsulates the game to server interaction.
-> Game Clients have a view into the game state
-> Battleship is the specified game
"""
import os
import random

class Game:
    """ This class encapsulates a game session. """
    _GAME_ID = -1
    _PLAYER1 = None
    _PLAYER2 = None
    _BATTLESHIP = None

    def __init__(self, p1, p2):
        self._GAME_ID = random.randrange(1000000)
        self._PLAYER1 = p1
        self._PLAYER2 = p2

    def start(self, player):
        """ Starts the game with the specified player"""
        print("")

    def start_game(self):
        """ Starts game after a coin toss to determine the starting player. """
        coin_toss = os.urandom(self._GAME_ID) % 2
        if coin_toss % 2 == 0:
            print("Player 1 wins the coin toss.")
        else:
            print("Player 2 wins the coin toss.")

