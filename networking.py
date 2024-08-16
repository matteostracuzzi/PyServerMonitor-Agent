import socket, json, struct
from threading import Thread
from main import settings
from enums import Enums
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

HEADER_SIZE = 4

# Custom socket to implement the communication protocol
class MyCustomSocket:
    def __init__(self, role:Enums.SocketRole) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((settings['master_ip'],settings['master_port']))
        
        self.key = None
        self.iv = None
        self.cypher = None

        data_to_send = bytes(json.dumps(dict(role=role)),'utf-8')
        self.send(data_to_send)
        
    
    def send(self, payload:bytes):

        payload = bytes(json.dumps(msg=payload,key=))

        if self.key and self.iv and self.cypher:
            payload = self.encrypt(payload)

        payload_length = len(payload)
        header = struct.pack('I', payload_length)
        msg = header + payload
        msg_length = len(msg)


        bytes_sent = 0
        while bytes_sent < msg_length:
            chunk = msg[:1024]
            n = self.socket.send(chunk)
            bytes_sent += n
            msg = msg[n:]

        return bytes_sent

    def receive(self):
        bytes_received = 0
        msg = b''
        while bytes_received < HEADER_SIZE:
            chunk = self.socket.recv(1024)
            if not chunk:
                return None
            bytes_received += len(chunk)
            msg += chunk

        header = msg[:HEADER_SIZE]
        payload_length = struct.unpack('I', header)[0]
        msg_length = HEADER_SIZE + payload_length


        while bytes_received < msg_length:
            chunk = self.socket.recv(1024)
            if not chunk:
                return None
            bytes_received += len(chunk)
            msg += chunk
        if self.key and self.iv:
            if not self.cypher:
                self.cypher = self.get_cypher(key=self.key,iv=self.iv)
            msg = self.decrypt(msg)
        self.key = msg['key']
        self.iv = msg['iv']

        return msg['data']

    @classmethod
    def get_cypher(cls, key:bytes,iv:bytes):
        return AES.new(key, AES.MODE_CBC, iv)


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
