
import graphviz

from system_designer import common

class Group:
    bgcolors = ( "#eaedef",  "#E5F5FD", "#FDF7E3", "#EBF3E7")
    group_attrs = {
        "shape": "box",
        "fontname": "Sans-Serif",
        "fontsize": "10",
        "fontcolor": "black",
        "margin": "20.0",
        "style": "filled",
        "color": "#eaedef",
        "fillcolor": "#eaedef",
        "labeljust": "l",
        "labelloc": "b",
    }
    def __init__(self, label, parent=None, **attrs):
        """Group class"""
        self.id = common.get_id()
        self.label = label
        self.parent = parent
        self.depth = self.parent.depth + 1 if self.parent else 0

        self.subgraph = graphviz.Digraph(name='cluster_%s' % self.id, graph_attr=self.group_attrs)
        self.subgraph.graph_attr["label"] = label

        if parent is not None:
            coloridx = self.depth % len(self.bgcolors)
            self.subgraph.graph_attr["pencolor"] = "white"
            self.subgraph.graph_attr["penwidth"] = "2.0"
            self.subgraph.graph_attr["fillcolor"] = self.bgcolors[coloridx]

        attrs = common.clean_attrs(attrs)
        self.subgraph.graph_attr.update(attrs)

    def add_node(self, node):
        """add a node in the group"""
        self.subgraph.node(node.id, **node.attrs)
    
    def add_group(self, group):
        """add subgraph to the group"""
        self.subgraph.subgraph(group)

def constructor(loader, node):
    """return yaml constructor"""
    return Group(**loader.construct_mapping(node))

