import pyautogui
import subprocess
from modules.event import Button, Type
from modules.utils import WithNumLock
from modules.window import Window
from modules.utils import ProcessExist
from modules.editor import Editor
from pathlib import Path
import os

window = Window()

class Default():
    def __init__(self):
        self.editor = Editor()
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
        self.editor.open()

    def runCalc(self, *aregs):
        if not ProcessExist('win32calc.exe'):
            windir = os.getenv('windir')
            subprocess.Popen([r'{}\system32\win32calc.exe'.format(windir)])
        else:
            window.ShowWindow('Calculator', 1000).join()

    def moveWindow(self, *args):
        WithNumLock(lambda *a: pyautogui.hotkey('shiftleft', 'shiftright', 'win', 'right'))

    def openShortcuts(self, *args):
        tryDirs = [Path(__file__).parent.parent.joinpath('personal/shortcuts'), Path(__file__).parent.parent.joinpath('shortcuts')]
        for directory in tryDirs:
            if not directory.exists():
                continue
            os.startfile(str(directory))
            window.ShowWindowAndMove('shortcuts', 1, 100, 100, 2000, 1000).join()
            break







