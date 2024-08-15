import socket, json
from threading import Thread
import base64
from main import settings
from enums import Enums

# Custom socket to implement the communication protocol
class MyCustomSocket:
    def __init__(self, role:Enums.SocketRole) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.connect((settings['master_ip'],settings['master_port']))
        socket.send(dict(role=role.value))
    
    def send(self, data:bytes):
        data = base64(data)
        self.socket.sendall(data)   # dump implementation
        return data

    def receive(self):
        return self.socket.recv(1024)

    @classmethod
    def get_cypher(cls, key):
        return None # implement a cypher that uses AES with the CBC mode


# The sender is the one who send the configured data to the master
class Sender:
    def __init__(self) -> None:
        self.socket = MyCustomSocket(role=Enums.SocketRole.SENDER)


# The receiver get the commands that the master want to execute on the device
class Receiver(Thread):
    def __init__(self) -> None:
        super().__init__()

    def run(self) -> None:
        self.socket = MyCustomSocket(role=Enums.SocketRole.RECEIVER)
