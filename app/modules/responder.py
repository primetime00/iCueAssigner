import pyautogui
from modules.constants import DEFAULT_KEYS
from modules.event import Button, Type, Event
from modules.processes import getProcessMap, fillResponderMap, setRequestFunction
from queue import Queue

from modules.window import Window

window = Window()

class Responder:
    def __init__(self, queue: Queue):
        self.funcMap = {}
        self.eventQueue = queue
        setRequestFunction(self.requestData)
        self.requestData()

    def requestData(self):
        self.eventQueue.put(Event(Type.RELOAD, Button.NONE, self.loadData))

    def loadData(self):
        fillResponderMap(self.showErrors)
        self.funcMap = {
            Button.M12: {
                Type.LONGPRESS: {'function': self.displayHelp, 'help': 'This help'},
            },
        }
        respondMap = getProcessMap()
        if DEFAULT_KEYS in respondMap:
            for button, types in respondMap[DEFAULT_KEYS]['functions'].items():
                if button not in self.funcMap:
                    self.funcMap[button] = {}
                for type, action in respondMap[DEFAULT_KEYS]['functions'][button].items():
                    self.funcMap[button][type] = action


    def key(self, eventType, button, proc, text):
        respondMap = getProcessMap()
        if proc in respondMap:
            functions = respondMap[proc]['functions']
            if button in functions and eventType in functions[button]:
                respondMap[proc]['functions'][button][eventType]['function'](eventType, button, proc, text)
                return

        if button in self.funcMap and eventType in self.funcMap[button]:
            self.funcMap[button][eventType]['function'](eventType, button, proc, text)

    def help(self, *args):
        helpData = {}
        respondMap = getProcessMap()
        for button, types in self.funcMap.items():
            helpData[button] = {}
            for type, action in self.funcMap[button].items():
                helpData[button][type] = self.funcMap[button][type]['help']

        if len(args) >= 4:
            proc = args[2]
            if proc in respondMap:
                for button, types in respondMap[proc]['functions'].items():
                    if button not in helpData:
                        helpData[button] = {}
                    for type, action in respondMap[proc]['functions'][button].items():
                        helpData[button][type] = '({}) {}'.format(respondMap[proc]['name'], respondMap[proc]['functions'][button][type]['help'])
        return helpData

    def displayHelp(self, *args):
        helpMap = self.help(*args)
        msg = ""
        for key in sorted(helpMap.keys()):
            val = helpMap[key]
            if type(val) is not dict:
                continue
            for key2, val2 in val.items():
                msg += Button.text(key)
                msg += ': '
                msg += Type.text(key2) + ' - ' + val2 + '\n'

        if len(args) >= 4:
            msg += '\n\n'
            msg += 'Current window process: '
            msg += '[{}]\n'.format(args[2])
            msg += '{}'.format(args[3])
        title = 'iCue Assigner'
        cw = window.ShowWindow(title, 1)
        pyautogui.alert(msg, title)
        cw.join()

    def showErrors(self, errors):
        msg = ""
        for i in range(0, len(errors)):
            error = errors[i]
            msg += error
            if i < len(errors)-1:
                msg += '\n------------------------------------------\n'
        title = 'iCue Assigner Script Error'
        cw = window.ShowWindow(title, 1)
        pyautogui.alert(msg, title)
        cw.join()








