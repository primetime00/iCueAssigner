from pathlib import Path
import json
import subprocess
import os

winDir = os.environ['WINDIR']

class Editor:
    defaultEditor = 'Notepad'
    defaultExe = winDir + '/System32/notepad.exe'
    defaultParams = []
    confFile = 'editor.json'

    def __init__(self):
        self.conf = Path(self.confFile)
        self.confMap = {'editor': self.defaultEditor, 'exe': self.defaultExe, 'params': self.defaultParams}
        if not self.conf.exists():
            with open(self.confFile, 'wt') as cf:
                json.dump(self.confMap, cf)
        else:
            with open(self.confFile, 'rt') as cf:
                self.confMap = json.load(cf)


    def open(self, file=None, useParams=True, extraParams=None):
        if extraParams is None:
            extraParams = []
        p = [self.confMap['exe']]
        if useParams and len(self.confMap['params']) > 0:
            for item in self.confMap['params']:
                p.append(item)
        if extraParams and len(extraParams) > 0:
            for item in extraParams:
                p.append(item)
        if file:
            p.append(file)
        subprocess.Popen(p)







