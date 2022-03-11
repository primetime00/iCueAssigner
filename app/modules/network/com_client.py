import jsonpickle
import serial.tools.list_ports as lp
import threading
import serial, time


class ComClient(threading.Thread):

    @staticmethod
    def getPorts():
        ports = lp.comports()
        ls = []
        for port, desc, hwid in sorted(ports):
            ls.append(port)
        return ls

    def __init__(self, queue, port):
        super().__init__(target=self.loop)
        self.comPort = port
        self.queue = queue
        self.done = False

    def quit(self):
        self.done = True


    def loop(self):
        ser = serial.Serial(port=self.comPort, baudrate=19200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS, timeout=0)
        incoming = ""
        while not self.done:
            time.sleep(0.2)
            serRead = ser.readline()
            if len(serRead) == 0:
                continue
            incoming += serRead.decode()
            idx = 0
            try:
                idx = incoming.rindex("|010")
            except ValueError:
                continue
            data = incoming[:idx]
            incoming = incoming[idx + 4:]
            lines = data.split("|010")
            if len(lines) > 0:
                for l in lines:
                    event = jsonpickle.decode(l)
                    self.queue.put(event)

        print("COM Client exit")
