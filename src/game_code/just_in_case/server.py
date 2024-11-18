
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
    
    def start_logging(self):
        self.logger = logging.getLogger('GameServer')
        self.logger.setLevel(logging.INFO)
        
        fh = logging.FileHandler('server.log')
        fh.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
    
    def load_questions(self) -> List[Dict]:
        try:
            with open('questions.txt', 'r') as f:
                questions = []
                for line in f:
                    split_result = re.split(r' \| ', line)
                    question = split_result[0]
                    answer = eval(split_result[1].strip())
                    entry = {"question": question, "answer": answer}
                    print(entry)
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

    def send_question(self, data):
        question = self.questions[self.current_question % len(self.questions)]
        question_message = json.dumps({
            "type": "question",
            "data": {"question": question["question"], "id": self.current_question}
        })
        data.outb += (question_message + "\n").encode()

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
                self.send_question(data)


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
                self.broadcast_scores()
            
            # send next question
            self.current_question += 1
            self.send_question(data)

    
    def service_connection(self, key: selectors.SelectorKey, mask: int):
        sock = key.fileobj
        data = key.data
        
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
                except ConnectionError:
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
    logger.addHandler(log_file_handler)

    return logger

if __name__ == "__main__":
    server = Server()
    server.run()
