from enum import IntEnum
import struct

class MessageType(IntEnum):
    INVALID = -1
    REQUEST_HOST = 0 # when client presses on host button
    REQUEST_JOIN = 1 # when client presses on join button, contains roomcode
    REPLY_ROOMCODE = 2 # sent from server to client, contains roomcode
    REPLY_IP = 3 # sent from server to client, contains ip of the host
    STATUS = 4

class LSP:
    def __init__(self): # when object is created initalizes the class variables with default values
        self.PROTOCOL_VERSION = 1
        self.MESSAGE_TYPE = MessageType.INVALID # invalid message
        self.message = [] # list of empty integers by default

    # self points to the current object
    # i -> signed
    # I -> Unsigned
    # ! -> network endianness which is big endian (as a analogy think about LTR vs RTL languages)
    '''
    This function returns the represtation of the class as bytes
    '''
    def encode(self):
        HEADER = struct.pack("!ii", self.PROTOCOL_VERSION, self.MESSAGE_TYPE)
        while len(self.message) > 0:
            val = self.message.pop(0)
            print(f"Val : {val}")
            HEADER += struct.pack("!I",  val)
        return HEADER

    '''
    This function converts the recieved bytes to class
    msg: Bytes
    '''
    def decode(self, msg):
        self.PROTOCOL_VERSION, self.MESSAGE_TYPE = struct.unpack("!ii", msg[0:8])
        msglen = len(msg) - 8
        # 4 over here is the integer size
        # i = 0 -> i = 4 -> i = 8
        for i in range(0, msglen, 4):
            self.appendMessage(struct.unpack("!I", msg[8 + i: 12 + i])[0])

    '''
    Setter for Message Type
    '''
    def setMessageType(self, msgType):
        self.MESSAGE_TYPE = int(msgType)

    '''
    Adds messages to a list for message Data
    '''
    def appendMessage(self, message: int):
        self.message.append(message)

    def getMessage(self):
        return self.message

    def clearMessage(self):
        self.message = []