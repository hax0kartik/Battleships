import socket
import random
import LSP
import ipaddress
from threading import Thread
from threading import Lock

HOST = ""
PORT = 9000

hosts = []

def connectionThread(lock, conn, addr):
    protocol = LSP.LSP()
    while True:
        data = conn.recv(1024)
        if not data:
            break
        protocol.decode(data)

        # parse Data
        if protocol.MESSAGE_TYPE == LSP.MessageType.REQUEST_HOST:
            # create a random int
            roomcode = random.randint(1000, 9999)
            with lock: # accquire lock
                hosts.append([addr, roomcode, False])

            # reply with roomcode
            protocol.setMessageType(LSP.MessageType.REPLY_ROOMCODE)
            protocol.clearMessage()
            protocol.appendMessage(roomcode)
            msg = protocol.encode()
            conn.sendall(msg)

        elif protocol.MESSAGE_TYPE == LSP.MessageType.REQUEST_JOIN:
            # Get roomcode
            roomcode = protocol.getMessage().pop(0)
            print(roomcode)
            print(hosts)

            # Check if we have a host with specified roomcode
            entry = -1
            with lock:
                for i in range(0, len(hosts)):
                    print(hosts[i][1], roomcode)
                    if hosts[i][1] == roomcode:
                        print("Found entry")
                        entry = i
                        break

            # Incase of valid roomcode, tell host it has a client
            with lock:
                if entry >= 0:
                    hosts[entry][2] = True
                    print(f"Client {addr} -> Server {hosts[entry][0]}")

            # reply with IP of host
            with lock:
                if entry >= 0:
                    hosts[entry][0]
                    protocol.setMessageType(LSP.MessageType.REPLY_IP)
                    protocol.clearMessage()
                    addr = int(ipaddress.ip_address(hosts[entry][0][0]))
                    print(addr)
                    protocol.appendMessage(addr)
                    msg = protocol.encode()
                    conn.sendall(msg)

    conn.close()


threadLock = Lock()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    while True:
        # accept call is blocking
        conn, addr = s.accept()
        print(f"Connected by {addr}")
        Thread(target=connectionThread, args=(threadLock, conn, addr)).start()
