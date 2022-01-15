import pyautogui
from modules.event import Button, Type

class Chrome():
    def __init__(self):
        self.keyMap = {
            'name': 'Chrome',
            'process': 'chrome.exe',
            'functions': {
                Button.M1: {
                    Type.KEYUP: {'function': self.back, 'help': 'Back'},
                },
                Button.M11: {
                    Type.KEYUP: {'function': self.newTab, 'help': 'Open A New Tab'},
                    Type.LONGPRESS: {'function': self.newIcogTab, 'help': 'Open Incognito Window'},
                },
                Button.M7: {
                    Type.KEYUP: {'function': self.nextTab, 'help': 'Next Tab'},
                },
                Button.M4: {
                    Type.KEYUP: {'function': self.prevTab, 'help': 'Previous Tab'},
                },
                Button.M8: {
                    Type.KEYUP: {'function': lambda *args: pyautogui.hotkey('pgdn'), 'help': 'Move Page Down'},
                    Type.LONGPRESS: {'function': lambda *args: pyautogui.hotkey('end'), 'help': 'Move To Bottom'},
                },
                Button.M9: {
                    Type.KEYUP: {'function': lambda *args: pyautogui.hotkey('pgup'), 'help': 'Move Page Up'},
                    Type.LONGPRESS: {'function': lambda *args: pyautogui.hotkey('home'), 'help': 'Move To Top'},
                },
                Button.M10: {
                    Type.KEYUP: {'function': self.closeTab, 'help': 'Close Tab'},
                    Type.LONGPRESS: {'function': self.reopen, 'help': 'Reopen Closed Tab'},
                },
            }
        }

    def back(self, *args):
        pyautogui.hotkey('alt', 'left')

    def reopen(self, *args):
        pyautogui.hotkey('ctrl', 'shift', 't')

    def nextTab(self, *args):
        pyautogui.hotkey('ctrl', 'pgdn')

    def prevTab(self, *args):
        pyautogui.hotkey('ctrl', 'pgup')

    def closeTab(self, *args):
        pyautogui.hotkey('ctrl', 'w')

    def newTab(self, *args):
        pyautogui.hotkey('ctrl', 't')

    def newIcogTab(self, *args):
        pyautogui.hotkey('ctrl', 'shift', 'n')









