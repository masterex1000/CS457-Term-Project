import sys
import selectors
import socket
import json
import logging
import re
import types
from typing import Dict, List

class Server:
    """ game server class used in the T/F game """
    def __init__(self, host: str = 'localhost', port: int = 42069):
        # setup logging
        self.logger = start_logging('Server')

        # stand up server
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.setblocking(False)
        self.server_sock.bind((host, port))
        self.server_sock.listen()

        # initialize selector and register server socket with selector
        self.sel = selectors.DefaultSelector()
        self.sel.register(self.server_sock, selectors.EVENT_READ, data=None)
        
        # Game state
        self.questions = self.load_questions()
        self.scores: Dict[str, int] = {}
        self.clients: Dict[socket.socket, types.SimpleNamespace] = {}
        self.current_question = 0
        
        self.logger.info(f"Server started on {host}:{port}")
        print(f"Server started on {host}:{port}")
    
    def load_questions(self) -> List[Dict]:
        try:
            with open('questions.txt', 'r') as f:
                questions = []
                for line in f:
                    split_result = re.split(r' \| ', line)
                    question = split_result[0]
                    answer = eval(split_result[1].strip())
                    entry = {"question": question, "answer": answer}
                    self.logger.info(f"Loading... {entry}")
                    questions.append(entry)
                self.logger.info(f"Loaded {len(questions)} questions from questions.txt")
                return questions
        except FileNotFoundError:
            self.logger.warning("questions.txt not found, using default questions")
            return [
                {"question": "TLS uses AES by default.", "answer": True},
                {"question": "TCP is a connectionless protocol.", "answer": False},
                {"question": "RAM is non-volatile memory.", "answer": False}
            ]
    
    def accept_connection(self, sock: socket.socket):
        conn, addr = sock.accept()
        self.logger.info(f"Accepted connection from {addr}")
        
        conn.setblocking(False)
        data = types.SimpleNamespace(
            addr=addr,
            username=None,
            inb=b"",
            outb=b"",
            messages_to_process=[],
        )
        
        # register connection for both reading and writing
        self.sel.register(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, data=data)
        self.clients[conn] = data
    
    def broadcast_scores(self):
        """ Share top N scores with all clients, updates all scoreboards"""
        top_n = 10
        top_scores = dict(sorted(self.scores.items(), key=lambda x: x[1], reverse=True)[:top_n])
        score_message = json.dumps({"type": "scores", "data": top_scores})
        
        # queue score update for all clients
        for client_data in self.clients.values():
            if client_data.username:
                client_data.outb += (score_message + "\n").encode()

    def declare_winner(self, username):
        """ Sends all clients a message letting them know who won and resets scores """
        win_message = json.dumps({"type": "winner", "data": {"username": username, "score": self.scores[username]}})

        # queue message for all clients
        for client_data in self.clients.values():
            if client_data.username:
                client_data.outb += (win_message + "\n").encode()

        # Reset scores
        self.scores = { x:0 for x in self.scores }

    def send_question(self, data, wasPrev = False, prevCorrect=False, currentScore=None):
        question = self.questions[self.current_question % len(self.questions)]
        
        question_message = {
            "type": "question",
            "data": {"question": question["question"], "id": self.current_question}
        }
        
        if wasPrev:
            question_message["data"]["prevCorrect"] = prevCorrect
            
        if currentScore is not None:
            question_message["data"]["currentScore"] = currentScore
        
        data.outb += (json.dumps(question_message) + "\n").encode()

    def process_message(self, sock: socket.socket, data: types.SimpleNamespace, message: dict):
        if message["type"] == "username":
            if not data.username:  # initial username registration
                username = message["data"]
                data.username = username
                self.scores[username] = 0
                self.logger.info(f"User {username} registered from {data.addr}")

                # Broadcast updated scores
                self.broadcast_scores()

                # send current question
                self.send_question(data, currentScore=self.scores[data.username])


        elif message["type"] == "answer" and data.username:
            question = self.questions[self.current_question % len(self.questions)]
            user_answer = message["data"]["answer"]
            correct_answer = question["answer"]
            answer_correct = user_answer==correct_answer
            
            self.logger.info(
                f"Player {data.username} answered {user_answer} "
                f"(correct answer was {correct_answer}) "
                f"to question: {question['question']}"
            )
            
            if answer_correct:
                self.scores[data.username] += 1
                
                # Check if we have a winner
                if self.scores[data.username] >= 10:
                    self.declare_winner(data.username)
                
                self.broadcast_scores()
            
            # send next question
            self.current_question += 1
            self.send_question(data, wasPrev=True, prevCorrect=answer_correct, currentScore=self.scores[data.username])

    
    # def service_connection(self, key: selectors.SelectorKey, mask: int):
    #     sock = key.fileobj
    #     data = key.data
        
    #     if mask & selectors.EVENT_READ:
    #         try:
    #             recv_data = sock.recv(1024)
    #             if recv_data:
    #                 data.inb += recv_data
                    
    #                 # Process complete messages
    #                 while b'\n' in data.inb:
    #                     message, data.inb = data.inb.split(b'\n', 1)
    #                     try:
    #                         decoded_message = json.loads(message.decode())
    #                         self.process_message(sock, data, decoded_message)
    #                     except json.JSONDecodeError:
    #                         self.logger.error(f"Invalid JSON received from {data.addr}")
    #             else:
    #                 # Connection closed by client
    #                 self.handle_disconnect(sock)
                    
    #         except ConnectionError:
    #             self.handle_disconnect(sock)
        
    #     if mask & selectors.EVENT_WRITE:
    #         if data.outb:
    #             try:
    #                 sent = sock.send(data.outb)
    #                 data.outb = data.outb[sent:]
    #             except ConnectionError:
    #                 self.handle_disconnect(sock)
    
    def service_connection(self, key: selectors.SelectorKey, mask: int):
        sock = key.fileobj
        data = key.data

        try:
            if mask & selectors.EVENT_READ:
                try:
                    recv_data = sock.recv(1024)
                    if recv_data:
                        data.inb += recv_data

                        # Process complete messages
                        while b'\n' in data.inb:
                            message, data.inb = data.inb.split(b'\n', 1)
                            try:
                                decoded_message = json.loads(message.decode())
                                self.process_message(sock, data, decoded_message)
                            except json.JSONDecodeError:
                                self.logger.error(f"Invalid JSON received from {data.addr}")
                    else:
                        # Connection closed by client
                        self.handle_disconnect(sock)

                except ConnectionError:
                    self.handle_disconnect(sock)

            if mask & selectors.EVENT_WRITE:
                if data.outb:
                    try:
                        sent = sock.send(data.outb)
                        data.outb = data.outb[sent:]
                    except (ConnectionError, OSError):
                        self.logger.error(f"Error sending data to {data.addr}")
                        self.handle_disconnect(sock)

        except (KeyError, ValueError):
            # KeyError occurs if the socket is unregistered during the process
            # self.logger.warning(f"Tried to process a closed connection for {sock.getpeername()}")
            pass
        except OSError as e:
            self.logger.error(f"OSError: {e}")
            self.handle_disconnect(sock)
    
    def handle_disconnect(self, sock: socket.socket):
        data = self.clients[sock]
        self.logger.info(f"Closing connection to {data.addr}")
        
        if data.username and data.username in self.scores:
            del self.scores[data.username]
            self.broadcast_scores()
        
        self.sel.unregister(sock)
        sock.close()
        del self.clients[sock]
    
    def run(self):
        self.logger.info("Server is now accepting connections")
        try:
            while True:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:  # Server socket
                        self.accept_connection(key.fileobj)
                    else:  # Client socket
                        self.service_connection(key, mask)
        except KeyboardInterrupt:
            self.logger.info("Server shutting down")
        finally:
            self.sel.close()

def start_logging(name):
    """ does what it says on the tin. """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    log_file_handler = logging.FileHandler('server.log')
    log_file_handler.setLevel(logging.INFO)

    ymd_hms_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    log_file_handler.setFormatter(ymd_hms_formatter)
    
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(log_file_handler)

    return logger

if __name__ == "__main__":
    
    if len(sys.argv) <= 2:
        server = Server()
    else:
        server = Server(sys.argv[1], int(sys.argv[2]))
    server.run()
