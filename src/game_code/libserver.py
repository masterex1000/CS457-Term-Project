
import sys
import selectors
import json
import io
import struct
from message import Message
from connection import Connection

class ServerConnection(Connection):
    def __init__(self, selector, sock, addr):
        Connection.__init__(self, selector, sock, addr)
    
    def on_message(self, message):
        action = message.get("action")
        if action == "message":
            msg = message.get("value")
            content = {"result": msg}
        else:
            content = {"result": f'Error: invalid action "{action}".'}
        
        self.send_message(content)
