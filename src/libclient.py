
import asyncio
import sys
import selectors
import json
import io
import struct
from message import Message
from connection import Connection

class ClientConnection(Connection):
    def __init__(self, selector, sock, addr):
        Connection.__init__(self, selector, sock, addr)
        
    def on_message(self, message):
        result = message.get("result")
        print(f"got result: {result}")
        pass
    
    async def ainput(string: str) -> str:
        await asyncio.to_thread(sys.stdout.write, f'{string} ')
        return await asyncio.to_thread(sys.stdin.readline)
    
    
    def on_connection(self):
        print("Connected to server")
        
    