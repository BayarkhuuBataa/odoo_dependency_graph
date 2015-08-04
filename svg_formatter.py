__author__ = 'colinwren'

from dependency_graph import DependencyGraph
from treelib import Tree
import svgwrite

class SvgFormatter:

    def __init__(self, dependency_graph):
        if isinstance(dependency_graph, DependencyGraph):
            self.graph = dependency_graph.hierarchy
        else:
            raise TypeError('Supplied dependency graph is not of class DependencyGraph')

    def convert_hierarchy_to_svg(self):
        if isinstance(self.graph, Tree):
            svg_document = svgwrite.Drawing(filename='{0}_dependency_graph.svg'.format(self.graph.root),
                                            size=('800px', '600px'))
            return svg_document
        else:
            raise TypeError('Supplied graph is not of class Tree')