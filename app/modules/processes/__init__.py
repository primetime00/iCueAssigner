import time
from importlib import import_module
import inspect, functools, sys
from modules.constants import DEFAULT_KEYS, USER_DIR
import traceback
import gc

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from pathlib import Path

responderModules = {}
_fileObserver = None
_lastEventTime = 0
_failures = []
_failureFunction = None
_requestFunc = None
_instanceList = []

def get_class_that_defined_method(meth):
    if isinstance(meth, functools.partial):
        return get_class_that_defined_method(meth.func)
    if inspect.ismethod(meth) or (inspect.isbuiltin(meth) and getattr(meth, '__self__', None) is not None and getattr(meth.__self__, '__class__', None)):
        for cls in inspect.getmro(meth.__self__.__class__):
            if meth.__name__ in cls.__dict__:
                return cls
        meth = getattr(meth, '__func__', meth)  # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        cls = getattr(inspect.getmodule(meth),
                      meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0],
                      None)
        if isinstance(cls, type):
            return cls
    return getattr(meth, '__objclass__', None)  # handle special descriptor objects


def setRequestFunction(func):
    global _requestFunc
    _requestFunc = func

def onFileChanged(event):
    global _lastEventTime
    systemTime = time.time()
    if systemTime - _lastEventTime > 0.1:
        if _requestFunc:
            _requestFunc()
        _lastEventTime = systemTime

def createWatcher():
    global _fileObserver
    if _fileObserver:
        return
    eventHandler = PatternMatchingEventHandler(['*.py'], None, True, False)
    eventHandler.on_any_event = onFileChanged
    _fileObserver = Observer()
    path = Path(__file__).parent.parent.parent.joinpath(USER_DIR)
    _fileObserver.schedule(eventHandler, str(path), recursive=False)
    _fileObserver.start()


def getFailures():
    return _failures


def fillResponderMap(failFunc=None):
    global _failures, _failureFunction, responderModules, _instanceList

    if failFunc:
        _failureFunction = failFunc
    _failures.clear()
    for f in Path(__file__).parent.glob("*.py"):
        if "__" in f.stem:
            continue
        import_module(__package__ + f".{f.stem}", __package__)

    while len(_instanceList) > 0:
        modName = _instanceList[0].__module__
        del _instanceList[0]
        if modName in sys.modules:
            del sys.modules[modName]

    responderModules.clear()
    _instanceList.clear()

    modList = []

    for f in Path(__file__).parent.parent.parent.joinpath(USER_DIR).glob("*.py"):
        if "__" in f.stem:
            continue
        modName =  USER_DIR + f".{f.stem}"
        if modName in sys.modules:
            del sys.modules[modName]
        try:
            modList.append(import_module(modName, USER_DIR))
        except Exception as e:
            _failures.append(traceback.format_exc(1))
    #del import_module, Path

    gc.collect()

    for mod in modList:
        classList = [x[1] for x in inspect.getmembers(mod, inspect.isclass) if x[1].__module__ == mod.__name__]
        for cls in classList:
            instance = cls()
            _instanceList.append(instance)
            keyMapData = getattr(instance, "keyMap", None)
            if type(keyMapData) != dict:
                continue
            if 'name' not in keyMapData:
                continue
            if 'functions' not in keyMapData:
                continue
            if 'process' in keyMapData:
                procData = keyMapData['process']
                if isinstance(procData, str):
                    procName = procData if len(procData) > 0 else DEFAULT_KEYS
                    responderModules[procName] = {'name': keyMapData['name'], 'functions': keyMapData['functions']}
                elif isinstance(procData, list) or isinstance(procData, tuple):
                    for p in procData:
                        procName = p if len(p) > 0 else DEFAULT_KEYS
                        responderModules[procName] = {'name': keyMapData['name'], 'functions': keyMapData['functions']}
            del keyMapData, instance
        del classList
    del modList

    createWatcher()
    if len(_failures) > 0 and _failureFunction:
        _failureFunction(_failures)

def getProcessMap():
    return responderModules





