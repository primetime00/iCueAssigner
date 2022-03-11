import socket
import threading
import traceback

import jsonpickle


class Client(threading.Thread):
    host = '192.168.1.228'
    port = 25700

    INIT = -1
    CONNECT = 0
    WAIT = 1
    PROCESS = 2
    QUIT = 3

    def __init__(self, queue, name=None, host=None, port=None):
        super().__init__(target=self.loop)
        self.socket = None
        if host:
            self.host = host
        if port:
            self.port = port
        self.queue = queue
        self.state = self.INIT
        self.breakEvent = threading.Event()
        self.name = name

    def sendInfo(self):
        data = ClientData(name=self.name if self.name else "_default")
        self.socket.send(jsonpickle.encode(data).encode())

    def quit(self):
        self.socket.close()
        self.breakEvent.set()

    def waitForConnect(self):
        self.breakEvent.wait(timeout=5)
        if self.breakEvent.is_set(): #we broke from something else - quit
            self.state = self.QUIT
            return
        self.state = self.CONNECT

    def loop(self):
        while True:
            if self.state == self.INIT:
                self.socket = socket.socket()
                self.state = self.CONNECT
            elif self.state == self.CONNECT:
                self.connect()
            elif self.state == self.WAIT:
                self.waitForConnect()
            elif self.state == self.PROCESS:
                self.process()
            elif self.state == self.QUIT:
                self.socket.close()
                break

    def connect(self):
        print('Waiting for connection')
        try:
            print("Connecting to: ", (self.host, self.port))
            self.socket.connect((self.host, self.port))
        except socket.error as e:
            print("Didn't connect, trying again")
            self.state = self.WAIT
            return
        print("Connected to: ", (self.host, self.port))
        #connection was made
        self.state = self.PROCESS

    def process(self):
        self.sendInfo()
        resp = None
        try:
            resp = self.socket.recv(1024)
            if len(resp) == 0:  # EOF, disconnected?
                self.socket.close()
                self.state = self.INIT
                return
        except ConnectionAbortedError:
            print("Lost connection...")
            self.socket.close()
            self.state = self.INIT
            return
        except Exception as e:
            print("Lost connection...")
            self.socket.close()
            self.state = self.INIT
            return
        #process resp
        event = jsonpickle.decode(resp)
        self.queue.put(event)

class ClientData:
    def __init__(self, name):
        self.name: str = name
        self.ip: str = ""
        self.port: int = 0

    def getName(self):
        return self.name

    def setNetwork(self, ip: str, port: int):
        self.ip = ip
        self.port = port