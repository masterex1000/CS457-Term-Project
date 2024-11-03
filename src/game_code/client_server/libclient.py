
import sys
import selectors
import json
import io
import struct
from message import Message
from connection import Connection

class ClientConnection(Connection):
    def __init__(self, selector, sock, addr, request):
        Connection.__init__(self, selector, sock, addr)
        
        self.response = None
        self._request_queued = False
        self.request = request

    def _process_response_json_content(self):
        content = self.response
        result = content.get("result")
        print(f"got result: {result}")

    def _process_response_binary_content(self):
        content = self.response
        print(f"got response: {repr(content)}")

    def write(self):
        if not self._request_queued:
            self.queue_request()

        self._write()

        if self._request_queued:
            if not self._send_buffer:
                # Set selector to listen for read events, we're done writing.
                self._set_selector_events_mask("r")

    def queue_request(self):
        content = self.request["content"]
        content_type = self.request["type"]
        content_encoding = self.request["encoding"]
        if content_type == "text/json":
            req = {
                "content_bytes": Message.json_encode(content, content_encoding),
                "content_type": content_type,
                "content_encoding": content_encoding,
            }
        else:
            req = {
                "content_bytes": content,
                "content_type": content_type,
                "content_encoding": content_encoding,
            }
        message = Message.create_message(**req)
        self._send_buffer += message
        self._request_queued = True

    def process_response(self):
        content_len = self.jsonheader["content-length"]
        if not len(self._recv_buffer) >= content_len:
            return
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]
        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            self.response = Message.json_decode(data, encoding)
            print("received response", repr(self.response), "from", self.addr)
            self._process_response_json_content()
        else:
            # Binary or unknown content-type
            self.response = data
            print(
                f'received {self.jsonheader["content-type"]} response from',
                self.addr,
            )
            self._process_response_binary_content()
        # Close when response has been processed
        self.close()
