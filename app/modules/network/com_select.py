from tkinter import Listbox, Frame, Button, TOP, StringVar, Tk
from threading import Thread

class ComSelect():

    def __init__(self, ports, resultFunc, selection=''):
        # Create object
        self.ports = ports
        self.resultFunc = resultFunc
        self.selection = selection

    def init(self):
        self.root = Tk()
        self.root.geometry('500x500')
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        self.clicked = StringVar()

        self.options = self.ports
        self.options.insert(0, 'Disable')


        self.root.title("COM Port Selection")
        self.original = ""

        self.drop = Listbox(self.root)
        self.drop.insert(0, *self.options)
        self.drop.pack(fill='y', pady=30)
        self.drop.bind('<<ListboxSelect>>', self.onselect)

        if self.selection not in self.options:
            self.drop.select_set(0)
            self.clicked.set(self.options[0])
        else:
            pos = self.options.index(self.selection)
            self.clicked.set(self.options[pos])
            self.drop.select_set(pos)

        self.frame = Frame(self.root)
        self.frame.pack(fill='x', expand=True)


        # Create button, it will change label text
        self.ok_button = Button(self.frame, text="OK", command=self.confirm).pack(side=TOP, fill='x', pady=1)
        self.cancel_button = Button(self.frame, text="Cancel", command=self.cancel).pack(side=TOP, fill='x', pady=5)


    def cancel(self):
        self.clicked.set(self.original)
        self.root.destroy()
        pass

    def confirm(self):
        if self.resultFunc:
            self.resultFunc(self.clicked.get())
        self.root.destroy()
        pass

    def onselect(self, evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.clicked.set(value)

    def run(self):
        self.init()
        self.root.mainloop()

    def getResult(self):
        return self.clicked.get()