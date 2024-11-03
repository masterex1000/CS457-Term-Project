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

    def __init__(self, game_id, p1, p2):
        self._GAME_ID = game_id
        self._PLAYER1 = p1
        self._PLAYER2 = p2

    def start(self, player):
        """ Starts the game with the specified player going first"""
        print("")

    def start_game(self):
        """ Starts game after a coin toss to determine the starting player. """
        coin_toss = os.urandom(self._GAME_ID) % 2
        if coin_toss % 2 == 0:
            print("Player 1 wins the coin toss.")
            self.start(self._PLAYER1)
        else:
            print("Player 2 wins the coin toss.")
            self.start(self._PLAYER2)
