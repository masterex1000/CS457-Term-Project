import selectors
from message import Message
import struct


# General class that libserver and libclient both derive from
class Connection:
    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_buffer = b""
        self._send_buffer = b""
        self._jsonheader_len = None
        self.jsonheader = None
        
        self.response = None
        self._request_queued = False
        self.request = None
        
        self.send_queue = []
        self.recv_queue = []
    
    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw" or mode == "wr":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {repr(mode)}.")
        self.selector.modify(self.sock, events, data=self)
    
    # Reads the latest data into the local buffer
    def _read(self):
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            if data:
                self._recv_buffer += data
            else:
                raise RuntimeError("Peer closed.")
    
    # Sends as much data as our send buffer can currently handle
    def _write(self):
        if self._send_buffer:
            print("sending", repr(self._send_buffer), "to", self.addr)
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]
        
        # Our buffer is empty, we no longer care abour write events
        if len(self._send_buffer) == 0:
            self._set_selector_events_mask("r")
                
    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()
            
    def write(self):
        self._write()
    
    # Called whenever we need to read data
    def read(self):
        self._read()

        if self._jsonheader_len is None:
            self.process_protoheader()

        if self._jsonheader_len is not None:
            if self.jsonheader is None:
                self.process_jsonheader()

        if self.jsonheader:
            if self.response is None:
                self.process_message()
    
    def close(self):
        print("closing connection to", self.addr)
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print(
                f"error: selector.unregister() exception for",
                f"{self.addr}: {repr(e)}",
            )

        try:
            self.sock.close()
        except OSError as e:
            print(
                f"error: socket.close() exception for",
                f"{self.addr}: {repr(e)}",
            )
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None
    
    def process_protoheader(self):
        hdrlen = 2
        if len(self._recv_buffer) >= hdrlen:
            self._jsonheader_len = struct.unpack(
                ">H", self._recv_buffer[:hdrlen]
            )[0]
            self._recv_buffer = self._recv_buffer[hdrlen:]
    
    def process_jsonheader(self):
        hdrlen = self._jsonheader_len
        if len(self._recv_buffer) >= hdrlen:
            self.jsonheader = Message.json_decode(
                self._recv_buffer[:hdrlen], "utf-8"
            )
            self._recv_buffer = self._recv_buffer[hdrlen:]
            for reqhdr in (
                "byteorder",
                "content-length",
                "content-type",
                "content-encoding",
            ):
                if reqhdr not in self.jsonheader:
                    raise ValueError(f'Missing required header "{reqhdr}".')
    
    def process_message(self):
        content_len = self.jsonheader["content-length"]
        
        if not len(self._recv_buffer) >= content_len:
            return
        
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]
        
        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            response = Message.json_decode(data, encoding)
            print("received response", repr(response), "from", self.addr)

            self.on_message(response)
        else:
            # Binary or unknown content-type
            print(
                f'received {self.jsonheader["content-type"]} response from',
                self.addr,
            )
            
            print(f"got response: {repr(data)}. Binary format currently unsupported. Ignoring")
    
    # Sends the given message to the peer
    def send_message(self, content):
        content_encoding = "utf-8"
        response = {
            "content_bytes": Message.json_encode(content, content_encoding),
            "content_type": "text/json",
            "content_encoding": content_encoding,
        }
        
        message = Message.create_message(**response)
        
        if len(message) > 0 and len(self._send_buffer) == 0:
            self._set_selector_events_mask("rw") # We care about write events now
        
        self._send_buffer += message
    
    # Called for every received message from the peer.
    def on_message(self, message):
        # Should this pass the message to the respective sub-system?
        # e.g. lobby requests to the lobby subsystem, game requests to the game subsystem etc.
        pass