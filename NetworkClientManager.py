from enum import IntEnum
import copy
import socket, ipaddress
import networking.LSP as LSP
import networking.GSP as GSP
from threading import Thread

class ClientEnums(IntEnum):
    HOST = 1
    CLIENT = 2
    UNKNOWN = 3

class NetworkClientManager:
    server_port = 9000
    host_port = 9001
    server_ip = "10.7.15.155"

    def __init__(self):
        self.roomcode = None
        self.connected = None
        self.host_ip = None
        self.mode = ClientEnums.UNKNOWN
        pass

    def SetMode(self, mode):
        self.mode = mode

    def GetMode(self):
        return self.mode

    def StartHostThreadFunc(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # TODO: This should listen on machine's ip address
        s.bind(('', self.host_port))
        s.listen()
        conn, addr = s.accept()
        msg = conn.recv(1024)
        protocol = GSP.GSP()
        protocol.decode(msg)
        if protocol.MESSAGE_TYPE == GSP.MessageType.HELLO:
            self.connected = True
            self.socket = conn

        protocol.setMessageType(GSP.MessageType.HELLO_ACK)
        bin = protocol.encode()
        conn.sendall(bin)

    def StartHost(self):
        protocol = LSP.LSP()
        protocol.setMessageType(LSP.MessageType.REQUEST_HOST)
        bin = protocol.encode()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server_ip, self.server_port))
            s.sendall(bin)
            msg = s.recv(1024)
            protocol.decode(msg)
            if protocol.MESSAGE_TYPE == LSP.MessageType.REPLY_ROOMCODE:
                self.roomcode = protocol.getMessage().pop(0)
            s.close()

        # start waiting for client to connect
        Thread(target=self.StartHostThreadFunc).start()

        return self.roomcode

    def IsConnected(self):
        return self.connected

    def StartJoin(self, roomcode: int):
        self.roomcode = roomcode
        protocol = LSP.LSP()
        protocol.setMessageType(LSP.MessageType.REQUEST_JOIN)
        protocol.appendMessage(roomcode)
        bin = protocol.encode()
        print(bin)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server_ip, self.server_port))
            s.sendall(bin)
            msg = s.recv(1024)
            protocol.decode(msg)
            if protocol.MESSAGE_TYPE == LSP.MessageType.REPLY_IP:
                self.host_ip = str(ipaddress.ip_address(protocol.getMessage().pop(0)))
                print(self.host_ip)
            s.close()

        protocol = GSP.GSP()
        protocol.setMessageType(GSP.MessageType.HELLO)
        bin = protocol.encode()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host_ip, self.host_port))
        s.sendall(bin)
        msg = s.recv(1024)
        protocol.decode(msg)
        if protocol.MESSAGE_TYPE == GSP.MessageType.HELLO_ACK:
            self.connected = True
            self.socket = s

    def IsArrangeDoneByClient(self):
        done = False
        protocol = GSP.GSP()
        protocol.setMessageType(GSP.MessageType.ARRANGE_STATUS)
        self.socket.sendall(protocol.encode())
        msg = self.socket.recv(1024)
        protocol.decode(msg)
        if protocol.MESSAGE_TYPE == GSP.MessageType.ARRANGE_STATUS_REPLY:
            done = bool(protocol.getMessage().pop(0))
        else:
            print(f"Unexpected message type {protocol.MESSAGE_TYPE}")

        return done

    def HandleArrangeStatus(self, status):
        protocol = GSP.GSP()
        msg = self.socket.recv(1024)
        protocol.decode(msg)
        if protocol.MESSAGE_TYPE == GSP.MessageType.ARRANGE_STATUS:
            protocol.setMessageType(GSP.MessageType.ARRANGE_STATUS_REPLY)
            protocol.appendMessage(int(status))
            msg = protocol.encode()
            self.socket.sendall(msg)
        elif protocol.MESSAGE_TYPE == GSP.MessageType.NEXT_SCREEN:
            return 1
            print(f"HandleArrangeStatus - Unexpected message type {protocol.MESSAGE_TYPE}")

        return 0

    def ChangeScreen(self):
        protocol = GSP.GSP()
        protocol.setMessageType(GSP.MessageType.NEXT_SCREEN)
        self.socket.sendall(protocol.encode())

    '''
    def SendAndRecieveGrid(self, grid):
        res = copy.deepcopy(grid)
        if self.mode == ClientEnums.CLIENT:
            protocol = GSP.GSP()
            protocol.setMessageType(GSP.MessageType.GRID)
            for i in len(0, len(grid)):
                for j in len(0, len(grid[i])):
                    protocol.appendMessage(grid[i][j])
            msg = protocol.encode()
            self.socket.sendall(msg)

            msg = self.socket.recv(1024)
            protocol.decode(msg)
            if protocol.MESSAGE_TYPE == GSP.MessageType.GRID_REPLY:
                for i in len(0, len(res)):
                    for j in len(0, len(res[i])):
                        res[i][j] = protocol.getMessage().pop(0)
        else:
            protocol = GSP.GSP()
            msg = self.socket.recv(1024)
            protocol.decode(msg)
            if protocol.MESSAGE_TYPE == GSP.MessageType.GRID:
                for i in len(0, len(res)):
                    for j in len(0, len(res[i])):
                        res[i][j] = protocol.getMessage().pop(0)

            protocol.setMessageType(GSP.MessageType.GRID_REPLY)
            for i in len(0, len(grid)):
                for j in len(0, len(grid[i])):
                    protocol.appendMessage(grid[i][j])
            msg = protocol.encode()
            self.socket.sendall(msg)

        return res
        '''

    def SetSocketToNonBlocking(self):
        self.socket.setblocking(False)

    def HandleGuess(self, checkCallback, args):
        protocol = GSP.GSP()
        flag = None
        try:
            msg = self.socket.recv(1024)
            protocol.decode(msg)
            if protocol.MESSAGE_TYPE == GSP.MessageType.GUESS:
                i = protocol.getMessage().pop(0)
                j = protocol.getMessage().pop(0)
                win, hit = checkCallback(*args, i, j)
                if win is True:
                    protocol.setMessageType(GSP.MessageType.WIN)
                else:
                    protocol.setMessageType(GSP.MessageType.GUESS_REPLY)
                    protocol.appendMessage(int(hit))
                msg = protocol.encode()
                self.socket.sendall(msg)

            elif protocol.MESSAGE_TYPE == GSP.MessageType.GUESS_REPLY:
                flag = protocol.getMessage().pop(0)
            elif protocol.MESSAGE_TYPE == GSP.MessageType.WIN:
                flag = 3
        except:
            pass

        return flag

    def SendGuess(self, i, j):
        protocol = GSP.GSP()
        protocol.setMessageType(GSP.MessageType.GUESS)
        protocol.appendMessage(i)
        protocol.appendMessage(j)
        msg = protocol.encode()
        self.socket.sendall(msg)
