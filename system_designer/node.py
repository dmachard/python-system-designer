
import os
import pathlib

from system_designer import common

class Node:
    node_attrs = {
        "shape": "box",
        "fontname": "Sans-Serif",
        "fontsize": "10",
        "fontcolor": "#2D3436",
        "style": "filled",
        "fillcolor": "white",
        "color": "#b3b5b5"
    }
    def __init__(self, label=None, kind=None, border=True, group=None, align="horizontal", **attrs):
        """Node class"""
        self.id = common.get_id()
        self.kind = kind
        self.group = group
        self.border = border
        self.attrs = self.node_attrs.copy()

        if label is None:
            label = ""
        self.label = label.replace("\n", "<br />")

        if not border:
            self.attrs["shape"] = "box"
            self.attrs["penwidth"] = "0.0"

        html_img = ""
        if kind is not None:
            icon = self.load_icon()
            if icon is not None: 
                html_img = """<td fixedsize="true" width="35" height="35"><img scale="true" src="%s" /></td>""" % icon
        
        html_rows = """<tr>
        %s<td>%s</td>
        </tr>""" % (html_img, self.label)

        if align=="vertical":
            html_rows = """<tr>
        %s</tr>
        <tr><td>%s</td></tr>
        """ % (html_img, self.label)

        self.attrs["label"] = """<
        <table cellspacing="0" border="0" cellborder="0">
        %s
        </table>>""" % html_rows

        attrs = common.clean_attrs(attrs)
        self.attrs.update(attrs)

    def load_icon(self):
        """load icon"""
        basedir = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
        file_path = os.path.join(basedir, "resources", "%s.png" % self.kind)
        if not pathlib.Path(file_path).is_file():
            return None
        return file_path

def constructor(loader, node) :
    """return yaml constructor"""
    return Node(**loader.construct_mapping(node))

