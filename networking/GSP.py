from enum import IntEnum
import struct

class MessageType(IntEnum):
    INVALID = -1
    HELLO = 0
    HELLO_ACK = 1
    ARRANGE_STATUS = 2
    ARRANGE_STATUS_REPLY = 3
    NEXT_SCREEN = 4
    GUESS = 7
    GUESS_REPLY = 8
    WIN = 9

class GSP:
    def __init__(self):
        self.PROTOCOL_VERSION = 1
        self.MESSAGE_TYPE = MessageType.INVALID
        self.message = []

    def encode(self):
        HEADER = struct.pack("!ii", self.PROTOCOL_VERSION, self.MESSAGE_TYPE)
        while len(self.message) > 0:
            HEADER += struct.pack("!i",  self.message.pop(0))
        return HEADER

    def decode(self, msg):
        self.PROTOCOL_VERSION, self.MESSAGE_TYPE = struct.unpack("!ii", msg[0:8])
        msglen = len(msg) - 8
        for i in range(0, msglen, 4):
            self.appendMessage(struct.unpack("!i", msg[8 + i: 12 + i])[0])

    def setMessageType(self, msgType):
        self.MESSAGE_TYPE = int(msgType)

    def appendMessage(self, message: int):
        self.message.append(message)

    def getMessage(self):
        return self.message

    def clearMessage(self):
        self.message = []