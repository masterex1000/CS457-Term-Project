
import socket
import json
import selectors
import sys
import types
from typing import Dict

class Client:

    def __init__(self, host= 'localhost', port= 42069):
        self.sel = selectors.DefaultSelector()
        self.running = True
        
        # Create client socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((host, port))
            print(f"Connected to server at {host}:{port}")
        except ConnectionRefusedError:
            print("Could not connect to server. Please ensure the server is running.")
            sys.exit(1)
        
        self.sock.setblocking(False)
        
        # Set up data storage
        self.data = types.SimpleNamespace(
            inb=b"",
            outb=b"",
            username=None
        )
        
        # Register socket for reading and writing
        self.sel.register(self.sock, selectors.EVENT_READ | selectors.EVENT_WRITE, data=self.data)
    
    def send_message(self, message: dict):
        """ queue a message to be sent to the server """
        self.data.outb += (json.dumps(message) + "\n").encode()
    
    def handle_username_input(self):
        """ get the username from player and send to server """
        username = input("Enter your username: ").strip()
        if username:
            self.data.username = username
            self.send_message({"type": "username", "data": username})
        else:
            print("Username cannot be empty. Please try again.")
            self.handle_username_input()
    
    def display_scores(self, scores: Dict[str, int]):
        """ prints the scoreboard """
        print("\n*** SCOREBOARD ***")
        for i, (player, score) in enumerate(scores.items(), 1):
            print(f"{i}. {player}: {score}")
        print("******************\n")

    def parse_in_buffer(self):
        """ parses the input buffer for messages """
        while b'\n' in self.data.inb:
            message, self.data.inb = self.data.inb.split(b'\n', 1)
            try:
                decoded_message = json.loads(message.decode())
                self.handle_message(decoded_message)
            except json.JSONDecodeError:
                print("Received invalid data from server")

    def handle_message(self, message: dict):
        """Process messages received from server"""
        if message["type"] == "question":
            print("\n" + "=" * 50)
            print("Question:", message["data"]["question"])

            answer = input("Your answer (T/F): ").strip().upper()
            if answer in ['T', 'F']:
                if answer=='T':
                    answer = True
                else:
                    answer = False

                self.send_message({
                    "type": "answer",
                    "data": {"answer": answer}
                })
            else:
                print("Invalid input. Please enter T or F.")
        
        elif message["type"] == "scores":
            self.display_scores(message["data"])

    def closed_connection(self):
        print("\nServer closed connection")
        self.running = False

    def lost_connection(self):
        print("\nLost connection to server")
        self.running = False

    def run(self):

        self.handle_username_input()
        
        try:
            while self.running:
                events = self.sel.select(timeout=1)
                for key, mask in events:
                    if mask & selectors.EVENT_READ:
                        try:
                            recv_data = self.sock.recv(1024)
                            if recv_data:
                                self.data.inb += recv_data
                                self.parse_in_buffer()
                            else:
                                self.closed_connection()
                                break
                        except ConnectionError:
                            self.lost_connection()
                            break
                    
                    if mask & selectors.EVENT_WRITE and self.data.outb:
                        try:
                            sent = self.sock.send(self.data.outb)
                            self.data.outb = self.data.outb[sent:]
                        except ConnectionError:
                            self.lost_connection()
                            break
        
        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            self.sel.unregister(self.sock)
            self.sock.close()
            self.sel.close()
            print("\nThank you for playing!")

if __name__ == "__main__":

    if len(sys.argv) <= 2:
        client = Client()
    else:
        client = Client(sys.argv[1], int(sys.argv[2]))

    client.run()
