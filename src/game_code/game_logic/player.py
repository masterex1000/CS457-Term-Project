"""
This file defines a player class which is just a data object representing player state
 ie. ID, Username, user token, private key
"""

class Player:
    """"""
    def __init__(self, user_id, username, user_token):
        self.user_id=user_id
        self.username=username
        self.user_token=user_token

