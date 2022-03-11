import queue
import time
from queue import Queue
from threading import Thread

import jsonpickle
import win32file
import win32pipe
import win32event
import pywintypes

from modules.event import Event, Type, Button

pipe_servers = {}

class PipeServer(Thread):

    INIT = 0
    PROCESS = 1
    QUIT = 2
    RESTART = 3
    CONNECT = 4


    def __init__(self, name):
        super().__init__(target=self.runner)
        self.totalConnections = 0
        self.pipe_name = name
        self.quit = False
        self.serverPipe = None
        self.started = False
        self.state = self.INIT
        self.connectEvent = None
        self.queue = Queue()

    def getName(self):
        return self.pipe_name


    def start(self) -> None:
        if self.started:
            return
        super().start()
        self.started = True

    def sendDataToClient(self, data):
        self.queue.put(data)

    def closeHandle(self):
        if self.serverPipe:
            win32file.CloseHandle(self.serverPipe)

    def initConnection(self):
        self.serverPipe = win32pipe.CreateNamedPipe(self.pipe_name, win32pipe.PIPE_ACCESS_DUPLEX | win32file.FILE_FLAG_OVERLAPPED, win32pipe.PIPE_TYPE_BYTE | win32pipe.PIPE_READMODE_BYTE | win32pipe.PIPE_WAIT, 1, 1024*64, 1024*64, 0, None)
        print("waiting for com connection", self.serverPipe)
        self.connectEvent = pywintypes.OVERLAPPED()
        self.connectEvent.hEvent = win32event.CreateEvent(None, 0, 0, None)
        win32pipe.ConnectNamedPipe(self.serverPipe, self.connectEvent)
        self.state = self.CONNECT

    def connect(self):
        rc = win32event.WaitForSingleObject(self.connectEvent.hEvent, 1000)
        if self.quit:
            self.state = self.QUIT
        if rc == 258: #timeout
            pass
        elif rc == 0: #connection made
            self.state = self.PROCESS

    def process(self):
        try:
            event: Event = self.queue.get(timeout=5)
        except queue.Empty: #check for connection
            try:
                win32pipe.PeekNamedPipe(self.serverPipe, 1)
            except pywintypes.error as e:
                print("restarting COM server due to disconnect")
                self.state = self.RESTART
            return
        eventType = event.getType()
        if eventType == Type.QUIT:
            print("Stopping pipe server", self.pipe_name)
            self.state = self.QUIT
        elif eventType == Type.RELOAD:
            pass
        else:  # pass it on to the client
            data = jsonpickle.encode(event) + "|010"
            try:
                win32file.WriteFile(self.serverPipe, data.encode())
            except pywintypes.error:
                self.state = self.RESTART

    def runner(self):
        while True:
            if self.state == self.INIT:
                self.initConnection()
            elif self.state == self.CONNECT:
                self.connect()
            elif self.state == self.PROCESS:
                self.process()
            elif self.state == self.QUIT:
                self.closeHandle()
                break
            elif self.state == self.RESTART:
                self.closeHandle()
                self.state = self.INIT

    def isStarted(self):
        return self.started


    def stop(self):
        if not self.started:
            return
        self.quit = True
        self.queue.put(Event(Type.QUIT, Button.NONE))