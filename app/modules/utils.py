import psutil
import modules.network as network
from modules.network.pipe_server import pipe_servers
from modules.event import Event, Button, Type
from win32process import GetWindowThreadProcessId
from win32gui import GetWindowText, GetForegroundWindow
from win32api import GetKeyState
from win32con import VK_NUMLOCK
import pyautogui


def GetWindowInfo():
    fw = GetForegroundWindow()
    tid, pid = GetWindowThreadProcessId(fw)
    try:
        proc = psutil.Process(pid=pid)
    except Exception:
        return None, None
    return proc.name(), GetWindowText(fw)

def ProcessExist(processName):
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def SendNetworkKeyEvent(name, eventType, key):
    if not network.server.isStarted():
        return
    network.server.sendDataToClient(name, Event(eventType, key, isRaw=False))

def SendPipeKeyEvent(pipeName, eventType, key):
    if pipeName not in pipe_servers:
        pipe_servers[pipeName] = network.PipeServer(name=pipeName)
        pipe_servers[pipeName].start()
    pipe_servers[pipeName].sendDataToClient(Event(eventType, key, isRaw=False))


def WithNumLock(func):
    hasNum = GetKeyState(VK_NUMLOCK) == 1
    if hasNum:
        pyautogui.press('numlock')
    func()
    if hasNum:
        pyautogui.press('numlock')
