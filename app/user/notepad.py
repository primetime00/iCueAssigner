import pyautogui
from modules.event import Button, Type

class Notepad():
    def __init__(self):
        self.keyMap = {
            'name': 'Notepad',
            'process': 'notepad.exe',
            'functions': {
                Button.M8: {
                    Type.KEYUP: {'function': lambda *args: pyautogui.hotkey('pgdn'), 'help': 'Move Page Down'},
                    Type.LONGPRESS: {'function': lambda *args: pyautogui.hotkey('ctrl', 'end'),
                                     'help': 'Move To Bottom'},
                },
                Button.M9: {
                    Type.KEYUP: {'function': lambda *args: pyautogui.hotkey('pgup'), 'help': 'Move Page Up'},
                    Type.LONGPRESS: {'function': lambda *args: pyautogui.hotkey('ctrl', 'home'), 'help': 'Move To Top'},
                },
                Button.M4: {
                    Type.KEYUP: {'function': lambda *args: pyautogui.hotkey('ctrl', 'alt', 'left'),
                                 'help': 'Back To Previous File'},
                },
                Button.M7: {
                    Type.KEYUP: {'function': lambda *args: pyautogui.hotkey('ctrl', 'alt', 'right'),
                                 'help': 'Forward To File'},
                },
            }
        }

