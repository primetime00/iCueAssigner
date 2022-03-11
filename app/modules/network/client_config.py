from tkinter import Button, StringVar, Tk, Entry, Label, Frame


class ClientConfig():

    @classmethod
    def valid(cls, name, url, port):
        if not name or len(name) == 0:
            return False
        if not url or len(url) == 0:
            return False
        if not port or len(port) == 0:
            return False
        try:
            int(port)
        except Exception:
            return False
        return True




    def __init__(self, resultFunc, data=None):
        # Create object
        self.port = data['port'] if data and 'port' in data else 0
        self.url = data['url'] if data and 'url' in data else ''
        self.name = data['name'] if data and 'name' in data else ''
        self.resultFunc = resultFunc

    def init(self):
        self.root = Tk()
        self.root.geometry('400x290')
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        self.nameVar = StringVar(value=self.name)
        self.urlVar = StringVar(value=self.url)
        self.portVar = StringVar(value=self.port)
        self.errorVar = StringVar()

        self.root.title("Client Setup")

        nameLbl = Label(self.root, text="Name:").place(x=30, y=50)
        urlLbl = Label(self.root, text="Host Name:").place(x=30, y=90)
        portLbl = Label(self.root, text="Host Port:").place(x=30, y=130)

        erX = 30
        erY = 240

        self.errorLbl = Label(self.root, fg='red', textvariable=self.errorVar)
        self.errorLbl.place(x=erX, y=erY)

        self.frame = Frame(self.root)
        self.frame.place(x=erX, y=erY, width=400, height =40)




        offset = 10

        sbmitBtn = Button(self.root, text="OK", width=7, command=self.confirm).place(x=110-offset, y=190)
        cencelBtn = Button(self.root, text="Cancel", width=7, command=self.cancel).place(x=230-offset, y=190)

        nameEntry = Entry(self.root, textvariable=self.nameVar).place(x=135, y=50)
        urlEntry = Entry(self.root, textvariable=self.urlVar).place(x=135, y=90)
        portEntry = Entry(self.root, textvariable=self.portVar).place(x=135, y=130)


    def cancel(self):
        self.root.destroy()
        pass

    def error(self, msg):
        self.errorVar.set(msg)
        self.errorLbl.lift(self.frame)
        self.root.after(2000, lambda: self.errorLbl.lower(self.frame))

    def confirm(self):
        if len(self.nameVar.get()) == 0 or len(self.urlVar.get()) == 0 or len(self.portVar.get()) == 0: #we are cancelling
            if self.resultFunc:
                self.resultFunc(None, None, None)
                self.root.destroy()
                return
        port = self.portVar.get()
        try:
            intPort = int(port)
        except Exception:
            self.error("Port needs to be a number.")
            return
        if self.resultFunc:
            self.resultFunc(self.nameVar.get(), self.urlVar.get(), intPort)
        self.root.destroy()

    def run(self):
        self.init()
        self.root.mainloop()

    def getResult(self):
        return self.clicked.get()