from modules.cue import iCue
from modules.responder import Responder
from modules.tray import SysTrayIcon
import os.path
import signal

import threading
import os
os.environ["PBR_VERSION"]="2"

from tendo import singleton

import sys
for x in list(sys.modules):
    if 'modules' in x:
        print(x)

class Main:
    def __init__(self):
        signal.signal(signal.SIGINT, self.breakHandler)
        self.trayIcon = None
        self.thread = threading.Thread(target=self.tray)
        self.thread.start()
        self.cue = iCue()
        queue = self.cue.getQueue()
        self.cue.setResponder(Responder(queue))
        self.cue.connect()
        self.cue.loop()
        self.thread.join()


    def tray(self):
        # menu_options = (('Exit', None, hello), )
        menu_options = ()
        cwd = os.path.dirname(os.path.realpath(__file__))
        self.trayIcon = SysTrayIcon(os.path.realpath(cwd + r'\resource\icon.ico'), 'iCue Assigner', menu_options, on_quit=self.quit)
        self.trayIcon.process()
        self.quit(None)

    def quit(self, icon):
        self.cue.exit()

    def breakHandler(self, signum, frame):
        print(1)
        self.trayIcon.end()
        print(2)
        self.cue.exit()
        #self.thread.join()


s = singleton.SingleInstance()
Main()








