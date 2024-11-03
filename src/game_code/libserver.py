
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
        
        self.request = None
        self.response_created = False

    def _create_response_json_content(self):
        action = self.request.get("action")
        if action == "message":
            message = self.request.get("value")
            content = {"result": message}
        else:
            content = {"result": f'Error: invalid action "{action}".'}
        content_encoding = "utf-8"
        response = {
            "content_bytes": Message.json_encode(content, content_encoding),
            "content_type": "text/json",
            "content_encoding": content_encoding,
        }
        return response

    def read(self):
        self._read()

        if self._jsonheader_len is None:
            self.process_protoheader()

        if self._jsonheader_len is not None:
            if self.jsonheader is None:
                self.process_jsonheader()

        if self.jsonheader:
            if self.request is None:
                self.process_request()

    def write(self):
        if self.request:
            if not self.response_created:
                self.create_response()

        self._write()


    def create_response(self):
        response = self._create_response_json_content()
        message = Message.create_message(**response)
        self.response_created = True
        self._send_buffer += message
