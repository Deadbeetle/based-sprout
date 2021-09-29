from xml import sax
from pydoc import locate
import tkinter

class Dummy:
    def __init__(self, master):
        self.master = master

class XmlTk(sax.ContentHandler):
    def __init__(self, filename, master=tkinter.Tk()):
        sax.ContentHandler.__init__(self)
        self.root = None
        self.current = master
        sax.parse(filename, self)

    def startDocument(self):
        pass

    def endDocument(self):
        pass

    def startElement(self, name, attrs):
        _ = dict()
        for k,v in attrs.items():
            if k == "command":
                _[k] = eval(v)
            else:
                _[k] = v
        attrs = _
        if name == "Tk":
            for k,v in attrs.items():
                getattr(self.current, k)(v)
        elif name == "grid":
            self.current.grid(**attrs)
            self.current = Dummy(self.current)
        else:
            self.current = locate("tkinter.{}".format(name))(self.current, **attrs)
            if not self.root:
                self.root = self.current
            self.current.grid()

    def endElement(self, name):
        self.current = self.current.master

