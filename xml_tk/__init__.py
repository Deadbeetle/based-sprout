from xml import sax
from pydoc import locate
import tkinter

class Dummy:
    """This class allows the use of XML tags that do not create a new Tk widget,
    such as the <grid /> tag for aligning widgets."""

    def __init__(self, master):
        self.master = master

# Converts tags into a tree of Tk widgets.
class XmlTk(sax.ContentHandler):
    def __init__(self, filename, master=tkinter.Tk()):
        """Creates a parser with self as the handler.

        :param filename: The name of the XML file to parse.
        :type filename: str
        :param master: The parent widget. If omitted, creates a new window.
        :type master: tkinter.Widget
        """
        sax.ContentHandler.__init__(self)
        self.root = None
        self.current = master
        self.named_widgets = dict()
        sax.parse(filename, self)

    def updateText(self, widgetname, stringvarname):
        """Helper function for updating text with buttons.

        :param widgetname: The name of the widget to update.
        :type widgetname: str
        :param stringvarname: The name of the StringVar to get the new text from.
        :type stringvarname: str
        """
        def action(widget=self.named_widgets[widgetname],
                   stringvar=self.named_widgets[stringvarname]):
            widget.config(text=stringvar.get())
        return action

    def startElement(self, name, attrs):
        """Determines whether to create a new widget and add it to the tree or to
        modify the last widget.

        :param name: The name of the XML tag.
        :type name: str
        :param attrs: The attributes of the XML tag.
        :type attrs: xml.sax.Attributes
        """

        # This section allows a name passed to the Button tag to be evaluated to
        # some function name. It could also be a lambda; please dont.
        widget_name = None
        _ = dict()
        for k,v in attrs.items():
            if k == "command":
                _[k] = eval(v)
            elif k == "name":
                widget_name = v
            elif k == "textvariable":
                if not v in self.named_widgets:
                    self.named_widgets[v] = tkinter.StringVar(self.root)
                _[k] = self.named_widgets[v]
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

        elif name == "StringVar":
            self.current = Dummy(self.current)
            var = tkinter.StringVar(**attrs)
            if widget_name:
                self.named_widgets[widget_name] = var

        # Create the widget, passing in the attributes as keyword arguments
        else:
            self.current = locate("tkinter.{}".format(name))(self.current, **attrs)
            if not self.root:
                self.root = self.current
            self.current.grid()
            if widget_name:
                self.named_widgets[widget_name] = self.current

    def endElement(self, name):
        """Go back up the tree in preperation to create the next widget.
        :param name: The name of the tag that is ending. Unused.
        :type name: str
        """
        self.current = self.current.master
