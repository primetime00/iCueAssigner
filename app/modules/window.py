from win32gui import FindWindow, MoveWindow, SetForegroundWindow
from threading import Thread
from time import sleep
from win32com.client import Dispatch

_dispatcher = Dispatch("WScript.Shell")

class Window:

    def __init__(self):
        pass

    def ShowWindow(self, title, timeout):
        _dispatcher.SendKeys('%')
        thread = Thread(target=self._showWindow, args=(title, timeout))
        thread.start()
        return thread

    def ShowWindowAndMove(self, title, timeout, x, y, w, h):
        _dispatcher.SendKeys('%')
        thread = Thread(target=self._showMoveWindow, args=(title, timeout, x, y, w, h))
        thread.start()
        return thread


    def _showWindow(self, title, timeout):
        hwnd = 0
        for i in range(0, 4*timeout, 1):
            hwnd = FindWindow(None, title)
            if hwnd == 0:
                sleep(0.25)
                continue
            else:
                break
        if hwnd == 0:
            return 0
        SetForegroundWindow(hwnd)
        return hwnd

    def _showMoveWindow(self, title, timeout, x, y, w, h):
        hwnd = self._showWindow(title, timeout)
        if hwnd > 0:
            MoveWindow(hwnd, x, y, w, h, True)






