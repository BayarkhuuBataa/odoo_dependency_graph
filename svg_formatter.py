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

    def convert_hierarchy_to_svg(self, width='2480px', height='3508px', margin=5, padding=1):
        if isinstance(self.graph, Tree):
            svg_document = svgwrite.Drawing(filename='{0}_dependency_graph.svg'.format(self.graph.root),
                                            size=(width, height))
            total_depth = self.graph.depth() + 1
            if margin < 0:
                raise ValueError('Supplied Margin is less than 0')
            # To get drawing area subtract both margins from height and width
            drawing_area = 100 - (margin * 2)

            # To get rect height divide the available space between the nodes
            rect_height = (drawing_area - (padding * total_depth)) / total_depth
            block_height = rect_height + (padding * 2)
            tree = self.graph
            for level in range(0, total_depth):
                nodes_at_depth = [tree[node] for node in tree.expand_tree() if tree.depth(node) == level]
                rect_width = (drawing_area - (padding * len(nodes_at_depth))) / len(nodes_at_depth)
                block_width = rect_width + padding
                for index, node in enumerate(nodes_at_depth):
                    leaf_insert_y = margin + ((total_depth - (level + 1)) * block_height)
                    leaf_insert_x = margin + (index * block_width)
                    kwargs = {"class": 'level-{0}'.format(level)}
                    svg_document.add(svg_document.rect(insert = ('{0}%'.format(leaf_insert_x),
                                                                 '{0}%'.format(leaf_insert_y)),
                                                       size = ('{0}%'.format(rect_width),
                                                               '{0}%'.format(rect_height)),
                                                       stroke_width = '0.5%',
                                                       stroke = 'black',
                                                       fill = 'rgb(255,255,255)',
                                                       **kwargs)
                                     )

                    text_offset_y = leaf_insert_y + (block_height/2)
                    text_offset_x = leaf_insert_x + (block_width/2)
                    svg_document.add(svg_document.text(node.tag,
                                                       insert = ('{0}%'.format(text_offset_x),
                                                                 '{0}%'.format(text_offset_y))
                                                       )
                                     )

            return svg_document
        else:
            raise TypeError('Supplied graph is not of class Tree')