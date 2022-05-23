
from system_designer import common

class Link:
    edge_attrs = {
        "color": "#676969",
        "fontcolor": "#676969",
        "fontname": "Sans-Serif",
        "fontsize": "10",
    }
    def __init__(self, origin, target, port="", description="", **attrs):
        """link class"""
        self.origin = origin
        self.target = target
        self.port = port
        self.description = description
        self.attrs = self.edge_attrs.copy()

        attrs = common.clean_attrs(attrs)
        self.attrs.update(attrs)

def constructor(loader, node) :
    """return a yaml constructor"""
    return Link(**loader.construct_mapping(node))