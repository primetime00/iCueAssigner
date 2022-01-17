import pyautogui
import subprocess
from modules.event import Button, Type
from win32api import GetKeyState
from win32con import VK_NUMLOCK
from modules.window import Window
from modules.utils import ProcessExist
from pathlib import Path
import os

window = Window()

class Default():
    def __init__(self):
        self.keyMap = {
            'name': 'Default',
            'process': '',
            'functions': {
                Button.M1: {
                    Type.KEYUP: {'function': self.moveWindow, 'help': 'Move Window To Next Monitor'},
                },
                Button.G1: {
                    Type.LONGPRESS: {'function': self.runNotepad, 'help': 'Open Notepad++'},
                },
                Button.G2: {
                    Type.LONGPRESS: {'function': self.runCalc, 'help': 'Open Calculator'},
                },
                Button.G6: {
                    Type.LONGPRESS: {'function': self.openShortcuts, 'help': 'Open Common Shortcuts'},
                },
            }
        }

    def runNotepad(self, *args):
        subprocess.Popen([r'C:\Program Files (x86)\Notepad++\notepad++.exe', '-nosession'])

    def runCalc(self, *aregs):
        if not ProcessExist('win32calc.exe'):
            windir = os.getenv('windir')
            subprocess.Popen([r'{}\system32\win32calc.exe'.format(windir)])
        else:
            window.ShowWindow('Calculator', 1000).join()

    def moveWindow(self, *args):
        hasNum = GetKeyState(VK_NUMLOCK) == 1
        if hasNum:
            pyautogui.press('numlock')
        pyautogui.hotkey('shiftleft', 'shiftright', 'win', 'right')
        if hasNum:
            pyautogui.press('numlock')
        pass

    def openShortcuts(self, *args):
        tryDirs = [Path(__file__).parent.parent.joinpath('personal/shortcuts'), Path(__file__).parent.parent.joinpath('shortcuts')]
        for directory in tryDirs:
            if not directory.exists():
                continue
            os.startfile(str(directory))
            window.ShowWindowAndMove('shortcuts', 1, 100, 100, 2000, 1000).join()
            break







