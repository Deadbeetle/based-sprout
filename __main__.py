import tkinter

class Application(tkinter.Frame):
    def __init__(self, title, master=None):
        tkinter.Frame.__init__(self, master)
        self.master.geometry("800x600")
        self.master.title(title)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.sampletext = tkinter.Label(self, text="This is a test window.")
        self.sampletext.grid()

def main():
    app = Application("Test")
    app.mainloop()

if __name__ == "__main__":
    main()
