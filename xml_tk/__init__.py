from xml import sax
from pydoc import locate
import tkinter

# This class allows the use of XML tags that do not create a new Tk widget,
# such as the <grid /> tag for aligning widgets.
class Dummy:
    def __init__(self, master):
        self.master = master

# Converts tags into a tree of Tk widgets.
class XmlTk(sax.ContentHandler):
    # Creates a parser with self as the handler.
    # @param filename The name of the XML file to parse.
    # @param master The parent widget. If omitted, creates a new window.
    def __init__(self, filename, master=tkinter.Tk()):
        sax.ContentHandler.__init__(self)
        self.root = None
        self.current = master
        sax.parse(filename, self)

    # Determines whether to create a new widget and add it to the tree or to
    # modify the last widget.
    # @param name The name of the XML tag.
    # @param attrs The attributes of the XML tag.
    def startElement(self, name, attrs):
        # This section allows a name passed to the Button tag to be evaluated to
        # some function name. It could also be a lambda; please dont.
        _ = dict()
        for k,v in attrs.items():
            if k == "command":
                _[k] = eval(v)
            else:
                _[k] = v
        attrs = _

        # The Tk tag is used to call functions on the master widget. Usually
        # this would be the window.
        if name == "Tk":
            for k,v in attrs.items():
                getattr(self.current, k)(v)

        # Unfortunately, alignment of widgets is a mutator instead of an
        # argument to the widget's constructor, so it needs a special tag
        elif name == "grid":
            self.current.grid(**attrs)
            self.current = Dummy(self.current)

        # Create the widget, passing in the attributes as keyword arguments
        else:
            self.current = locate("tkinter.{}".format(name))(self.current, **attrs)
            if not self.root:
                self.root = self.current
            self.current.grid()

    # Go back up the tree in preperation to create the next widget.
    # @param name The name of the tag that is ending. Unused.
    def endElement(self, name):
        self.current = self.current.master
