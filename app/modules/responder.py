import os.path
import sys

import pyautogui, traceback
from modules.constants import DEFAULT_KEYS
from modules.event import Button, Type, Event
from modules.processes import getProcessMap, fillResponderMap, setRequestFunction, getPersonalPath
from queue import Queue
import subprocess

from modules.window import Window
from pathlib import Path
import re
from modules.editor import Editor

window = Window()

class Responder:
    templatePath = Path(__file__).parent.parent.joinpath('resource')

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
        if proc and proc in respondMap:
            functions = respondMap[proc]['functions']
            if button in functions and eventType in functions[button]:
                try:
                    respondMap[proc]['functions'][button][eventType]['function'](eventType, button, proc, text)
                except Exception as e:
                    self.showErrors([traceback.format_exc()])
                return

        if button in self.funcMap and eventType in self.funcMap[button]:
            try:
                self.funcMap[button][eventType]['function'](eventType, button, proc, text)
            except Exception as e:
                self.showErrors([traceback.format_exc()])

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
                        helpData[button][type] = '({}) {}'.format(respondMap[proc]['name'],
                                                                  respondMap[proc]['functions'][button][type]['help'])
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
        proc = args[2]
        editButtonText = 'Edit' if proc in getProcessMap() else 'Create'
        res = pyautogui.confirm(msg, title, buttons=['OK', editButtonText])
        cw.join()
        if res == editButtonText:
            editor = Editor()
            if proc in getProcessMap():
                editor.open(file=getProcessMap()[proc]['file'])
            else:
                res = self.createNewResponder(proc, os.path.splitext(proc)[0])
                if res:
                    editor.open(file=res)

    def showErrors(self, errors):
        msg = ""
        for i in range(0, len(errors)):
            error = errors[i]
            msg += error
            if i < len(errors) - 1:
                msg += '\n------------------------------------------\n'
        title = 'iCue Assigner Script Error'
        cw = window.ShowWindow(title, 1)
        pyautogui.alert(msg, title)
        cw.join()

    def createNewResponder(self, process, name):
        i = 0
        base = self.camelCase(os.path.splitext(process)[0]).lower()
        fname = base + '.py'
        fpath = getPersonalPath().joinpath(fname)
        while fpath.exists():
            i += 1
            fname = base + '_' + i + '.py'
            fpath = getPersonalPath().joinpath(fname)

        if not self.templatePath.exists():
            print('Could not find template path', self.templatePath)
            return None
        templateFile = self.templatePath.joinpath('template.dat')
        if not templateFile.exists():
            print('Could not find template file')
            return None
        with open(templateFile, 'rt') as tmpFile:
            tempData = tmpFile.read()
            cname = self.camelCase(os.path.splitext(process)[0]).capitalize()
            tempData = tempData.replace('~CLASS~', cname)
            tempData = tempData.replace('~NAME~', name)
            tempData = tempData.replace('~PROCESS~', process)
            with open(fpath, 'wt') as dstFile:
                dstFile.write(tempData)
        return fpath

    def camelCase(self, tag_str):
        words = re.findall(r'\w+', tag_str)
        nwords = len(words)
        if nwords == 1:
            return words[0]  # leave unchanged
        elif nwords > 1:  # make it camelCaseTag
            return words[0].lower() + ''.join(map(str.title, words[1:]))
        return ''  # no word characters