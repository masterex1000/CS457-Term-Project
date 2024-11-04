import sys
import json
import io
import struct


class Message:
    def json_encode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

    def json_decode(self, json_bytes, encoding):
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        obj = json.load(tiow)
        tiow.close()
        return obj

    def create_message(
        self, *, content_bytes, content_type, content_encoding
    ):
        json_header = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
        }
        json_header_bytes = Message.json_encode(json_header, "utf-8")
        message_hdr = struct.pack(">H", len(json_header_bytes))
        message = message_hdr + json_header_bytes + content_bytes
        return message
