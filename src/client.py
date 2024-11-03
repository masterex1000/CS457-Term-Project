# TCP Client Reqs:
# - Connect to a server
# - Error handling
# - Log connection/disconnection
# - create and send message

#!/usr/bin/env python3

import asyncio
import sys
import socket
import selectors
import traceback
import struct

import libclient

sel = selectors.DefaultSelector()

def start_connection(host, port):
    addr = (host, port)
    print("starting connection to", addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = libclient.ClientConnection(sel, sock, addr)
    sel.register(sock, events, data=message)
    
    message.send_message({'action': "debug.message", 'value': 'blah'}) # Queue our first message

if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])

start_connection(host, port)

try:
    while True:
        events = sel.select(timeout=1)
        for key, mask in events:
            conn = key.data
            try:
                conn.process_events(mask)
            except Exception:
                print(
                    "main: error: exception for",
                    f"{conn.addr}:\n{traceback.format_exc()}",
                )
                conn.close()
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()

async def main():
    

if __name__ == "__main__":
    asyncio.run(main())