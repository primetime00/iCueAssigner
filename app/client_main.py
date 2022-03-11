import json
import os
import os.path
import signal
import threading
from queue import Queue, Empty

from modules.network.com_select import ComSelect
from modules.network.client_config import ClientConfig


from modules.network import Client
from modules.network import ComClient
from modules.event import Event, Type

from modules.responder import Responder
from modules.tray import SysTrayIcon
from modules.utils import GetWindowInfo

os.environ["PBR_VERSION"]="2"
from tendo import singleton
import sys

for x in list(sys.modules):
    if 'modules' in x:
        print(x)

class Main:
    def __init__(self):
        signal.signal(signal.SIGINT, self.breakHandler)
        self.currentData = None
        self.comSelectDialog = None
        self.netSelectDialog = None
        self.trayIcon = None
        self.done = False
        self.queue = Queue()
        self.responder = Responder(self.queue)
        self.loadData()
        self.thread = threading.Thread(target=self.tray)

        self.netClient = None
        self.thread.start()
        self.loadNetClient()
        self.comClient = None
        self.loadComClient()
        self.loop()
        self.thread.join()

    def loadComClient(self):
        data = self.loadData()
        if self.comClient and self.comClient.is_alive():
            print("Stopping Net Client")
            self.comClient.quit()
            self.comClient.join()
        if 'com' in data:
            cl = data['com']
            if cl not in ComClient.getPorts():
                return
            print("loading ", cl)
            self.comClient = ComClient(self.queue, cl)
            self.comClient.start()

    def loadNetClient(self):
        data = self.loadData()
        if self.netClient and self.netClient.is_alive():
            print("Stopping Net Client")
            self.netClient.quit()
            self.netClient.join()
        if 'net' in data:
            netData = data['net']
            if not ClientConfig.valid(netData['name'], netData['url'], str(netData['port'])):
                return
            print("loading client ", netData['name'], netData['url'], str(netData['port']))
            self.netClient = Client(queue=self.queue, name=netData['name'], host=netData['url'], port=int(netData['port']))
            self.netClient.start()




    def netSetup(self, icon):
        if not self.netSelectDialog:
            self.queue.put(Event(Type.CLIENT_NET, None))

    def netSelected(self, name, url, port):
        data = self.loadData()
        if not data:
            data = {}
        if not name or not url or not port:
            if 'net' in data:
                del data['net']
        else:
            data['net'] = {'name': name, 'url': url, 'port': int(port)}
        with open('settings.json', 'wt') as f:
            json.dump(data, f)
        self.queue.put(Event(Type.RELOAD, None, func=self.loadNetClient))

    def comSelect(self, icon):
        if not self.comSelectDialog:
            self.queue.put(Event(Type.CLIENT_COM, None))

    def comSelected(self, port):
        data = self.loadData()
        if not data:
            data = {}
        if port.strip() not in ComClient.getPorts():
            if 'com' in data:
                del data['com']
        else:
            data['com'] = port.strip()
        with open('settings.json', 'wt') as f:
            json.dump(data, f)
        self.queue.put(Event(Type.RELOAD, None, func=self.loadComClient))


    def tray(self):
        menu_options = ( ('Network Client Setup', None, self.netSetup), ('Serial Client Setup', None, self.comSelect),)
        cwd = os.path.dirname(os.path.realpath(__file__))
        self.trayIcon = SysTrayIcon(os.path.realpath(cwd + r'\resource\icon.ico'), 'iCue Assigner Client', menu_options, on_quit=self.quit)
        self.trayIcon.process()
        self.quit(None)

    def quit(self, icon):
        if self.netClient:
            self.netClient.quit()
        if self.comClient:
            self.comClient.quit()
        self.done = True

    def loop(self):
        while not self.done:
            try:
                event = self.queue.get(timeout=0.5)
            except Empty:
                continue
            proc, text = GetWindowInfo()
            type = event.getType()
            button = event.getButton()
            if type == Type.QUIT:
                self.quit(None)
            elif type == Type.RELOAD:
                if event.func:
                    event.func()
            elif type == Type.CLIENT_COM:
                self.comSelectDialog = ComSelect(ComClient.getPorts(), self.comSelected, selection=self.currentData['com'] if 'com' in self.currentData else '')
                self.comSelectDialog.run()
                self.comSelectDialog = None
            elif type == Type.CLIENT_NET:
                self.netSelectDialog = ClientConfig(self.netSelected, data=self.currentData['net'] if 'net' in self.currentData else None)
                self.netSelectDialog.run()
                self.netSelectDialog = None
            else:
                self.responder.key(type, button, proc, text)



    def breakHandler(self, signum, frame):
        self.trayIcon.end()
        if self.netClient:
            self.netClient.quit()
        if self.comClient:
            self.comClient.quit()

    def loadData(self):
        dataMap = {}
        if os.path.exists('settings.json'):
            with open('settings.json') as f:
                dataMap = json.load(f)
        self.currentData = dataMap
        return dataMap




s = singleton.SingleInstance()
Main()









