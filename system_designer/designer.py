import yaml
import graphviz
import os
import sys

from system_designer import common
from system_designer import group
from system_designer import node
from system_designer import link

class Design:
    graph_attr = {
        "layout":"dot",
        "compound":"true",
        "rankdir": "TB",
        "pad": "1.0",
        "splines": "ortho",
        "nodesep": "0.5",
        "ranksep": "1.5",
        "fontname": "Sans-Serif",
        "fontsize": "15",
    }
    legend = ("n°", "origin", "target", "protocol/port", "description")
    def __init__(self, name, groups=[], nodes=[], links=[], **attrs):
        """design class"""
        self.name = name
        self.groups = groups
        self.nodes = nodes
        self.links = links

        self.root_graph = graphviz.Digraph(name=name, graph_attr=self.graph_attr)
        self.root_graph.graph_attr["label"] = self.name

        attrs = common.clean_attrs(attrs)
        self.root_graph.graph_attr.update(attrs)

    def add_node(self, node):
        """add a node in the root graph"""
        self.root_graph.node(node.id, **node.attrs)

    def add_group(self, group):
        """add subgraph into the root graph"""
        self.root_graph.subgraph(group)

    def get_node_by_group(self, group):
        """search a node by group"""
        nodes = []
        for n in self.nodes:
            if n.group == group:
                nodes.append(n.id)
        return nodes

    def draw(self, output_file, output_format="png"):
        """draw the final architecture"""
        # reverse the list
        self.groups.reverse()

        # add element in group
        for node in self.nodes:
            if node.group: 
                node.group.add_node(node)
            else:
                self.add_node(node)

        # add groups
        for gr in self.groups:
            if gr.parent: 
                gr.parent.add_group(gr.subgraph)
            else:
                self.add_group(gr.subgraph)

        # finally add all links
        for i in range(len(self.links)):
            lnk = self.links[i] 
            lhead = ""; ltail = ""
            src = ""
            dst = ""

            if isinstance(lnk.target, group.Group):
                lhead = "cluster_%s" % lnk.target.id
                nodes = self.get_node_by_group(lnk.target)
                if len(nodes): dst = nodes[0]
            else:
                dst = lnk.target.id

            if isinstance(lnk.origin,  group.Group):
                ltail = "cluster_%s" % lnk.origin.id
                nodes = self.get_node_by_group(lnk.origin)
                if len(nodes): src = nodes[0]
            else:
                src = lnk.origin.id

            if len(src) and len(dst):
                xlabel = " %s " % (i+1)

                if lnk.port is not None:
                    xlabel += "\n%s " % lnk.port

                if "label" in lnk.attrs:
                    xlabel = lnk.attrs["label"]
                    del lnk.attrs["label"]

                self.root_graph.edge(src, dst, xlabel=xlabel, lhead=lhead, ltail=ltail, **lnk.attrs)

        # render the diagram
        self.root_graph.render(filename=output_file, format=output_format)
        # remove the graphviz file
        os.remove(output_file)

        # create html legend
        self.write_legend(output_file)

    def write_legend(self, output_file):
        """generate legend"""
        html_legend = [ """<!DOCTYPE html>
<html>
<head>
<style>
#matrix {
  font-family: Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

#matrix td, #matrix th {
  border: 1px solid #ddd;
  padding: 8px;
}

#matrix tr:nth-child(even){background-color: #f2f2f2;}

#matrix tr:hover {background-color: #ddd;}

#matrix th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #04AA6D;
  color: white;
}
</style>
</head>
<body>
""" ]
        html_legend.append("<table id=\"matrix\">")
        html_legend.append("<tr>")
        for col in self.legend:
            html_legend.append("<th>%s</th>" % col)
        html_legend.append("</tr>")

        for i in range(len(self.links)):
            lnk = self.links[i]
            html_legend.append("<tr>")
            html_legend.append("<td>%s</td>" % (i+1) )
            html_legend.append("<td>%s</td>" % lnk.origin.label)
            html_legend.append("<td>%s</td>" % lnk.target.label)
            html_legend.append("<td>%s</td>" % lnk.port)
            html_legend.append("<td>%s</td>" % lnk.description)
            html_legend.append("</tr>")
        html_legend.append("</table></body></html>")

        with open("%s.html" % output_file, "w") as f:
            f.write("\n".join(html_legend))

def design_constructor(loader, node) :
    """return yaml constructor"""
    return Design(**loader.construct_mapping(node))

def yaml_loader():
    """return specific yaml loader"""
    loader = yaml.SafeLoader
    loader.add_constructor("!design", design_constructor)
    loader.add_constructor("!gp", group.constructor)
    loader.add_constructor("!nd", node.constructor)
    loader.add_constructor("!lk", link.constructor)
    return loader

def generate(archi_file, output_file, output_format):
    """load the yaml file and draw the associated design"""
    try:
        with open(archi_file, "rb") as f:
            design = yaml.load(f, Loader=yaml_loader())
    except Exception as e:
        print(e)
    else:
        if design is None:
            print("invalid yaml file")
            sys.exit(1)

        # draw schema
        design["architecture"].draw(output_file, output_format)
