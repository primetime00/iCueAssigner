import queue
import sched, time, threading, random
import cuesdk
from cuesdk import CueSdk
from queue import Queue
from win32process import GetWindowThreadProcessId
from win32gui import GetWindowText, GetForegroundWindow
import psutil

from modules.event import Event, Button, Type
from modules.responder import Responder
from modules.constants import LONGPRESS_TIME

class iCue:
    def __init__(self):
        self.quit = False
        self.longPressTime = LONGPRESS_TIME
        self.schedulerEvent = threading.Event()
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.schedulerThread = threading.Thread(target=self.scheduleWorker, args=())
        self.eventQueue = Queue()

        self.sdk = CueSdk()
        self.deviceCount = 0
        self.currentKeys = {}
        self.responder: Responder = None
        pass

    def getQueue(self):
        return self.eventQueue

    def setResponder(self, responder: Responder):
        self.responder = responder

    def scheduleWorker(self):
        while not self.quit:
            self.schedulerEvent.wait()
            self.schedulerEvent.clear()
            self.scheduler.run()
        print("Schedule Exit")

    def handler(self, event_id, data):
        if event_id == cuesdk.CorsairEventId.KeyEvent:
            pressed = data.isPressed
            key = data.keyId
            self.processKey(key, pressed)
        pass

    def connect(self):
        self.schedulerThread.start()
        self.sdk.connect()
        self.deviceCount = self.sdk.get_device_count()
        self.displayInfo()
        self.sdk.subscribe_for_events(self.handler)

    def close(self):
        print("Closing SDK")
        self.sdk.unsubscribe_from_events()
        self.quit = True
        self.schedulerEvent.set()

    def displayInfo(self):
        print(self.sdk.protocol_details)
        print(self.sdk.get_devices())

    def generateID(self):
        return random.randint(0, 999999)

    def processKey(self, key, pressed):
        value = key.value
        keyState = (value, time.time(), random.randint(0, self.generateID()))
        if pressed:
            if value not in self.currentKeys:
                #we just pressed this key, set a time to see
                evt = Event(Type.KEYDOWN, value)
                if self.responder:
                    self.eventQueue.put(evt)
                self.scheduler.enter(self.longPressTime, 1, self.checkLong, (keyState, pressed, evt))
                self.currentKeys[value] = (keyState, pressed, evt)
        else:
            if value in self.currentKeys:
                if self.responder:
                    self.eventQueue.put(Event(Type.KEYUP, value))
                self.currentKeys.pop(value)
        self.schedulerEvent.set()

    def findEvent(self, value):
        if value in self.currentKeys:
            return self.currentKeys[value][2]
        return None

    def checkLong(self, state, pressed, event):
        value = state[0]
        id = state[2]
        #is the value still in the currentKey
        if value in self.currentKeys and self.currentKeys[value][0][2] == id:
            self.longPress(state)
            self.currentKeys.pop(value)


    def loop(self):
        while not self.quit:
            try:
                item = self.eventQueue.get(timeout=0.5)
            except queue.Empty:
                continue
            if self.responder:
                proc, text = self.getWindowInfo()
                type = item.getType()
                button = item.getButton()
                if type == Type.QUIT:
                    self.close()
                elif type == Type.RELOAD:
                    if item.func:
                        item.func()
                else:
                    self.responder.key(type, button, proc, text)
        print("Loop complete")

    def longPress(self, state):
        value = state[0]
        evt = self.findEvent(value)
        if self.responder and evt:
            self.eventQueue.put(Event(Type.LONGPRESS, state[0]))
            self.eventQueue.put(Event(Type.REMOVE, state[0]))

    def exit(self):
        self.eventQueue.put(Event(Type.QUIT, Button.NONE))

    def getWindowInfo(self):
        fw = GetForegroundWindow()
        tid, pid = GetWindowThreadProcessId(fw)
        try:
            proc = psutil.Process(pid=pid)
        except Exception:
            return None, None
        return proc.name(), GetWindowText(fw)




