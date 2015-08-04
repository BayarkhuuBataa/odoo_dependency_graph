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

            # To get the actual height take the padding times nodes (except the first)
            # then take away the stroke (0.5 * 2) from this
            actual_height = (drawing_area - (padding * (total_depth - 1))) - total_depth

            # To get rect height divide the available space between the nodes
            rect_height = actual_height / total_depth
            block_height = (rect_height + (padding * 2))
            tree = self.graph
            for level in range(0, total_depth):
                nodes_at_depth = [tree[node] for node in tree.expand_tree() if tree.depth(node) == level]
                for node in nodes_at_depth:
                    leaf_insert_y = (drawing_area - (level * block_height)) - total_depth
                    leaf_insert_x = margin
                    kwargs = {"class": 'level-{0}'.format(level)}
                    svg_document.add(svg_document.rect(insert = ('{0}%'.format(leaf_insert_x),
                                                                 '{0}%'.format(leaf_insert_y)),
                                                       size = ('{0}%'.format(drawing_area),
                                                               '{0}%'.format(rect_height)),
                                                       stroke_width = '0.5%',
                                                       stroke = 'black',
                                                       fill = 'rgb(255,255,255)',
                                                       **kwargs)
                                     )

                    text_offset_y = leaf_insert_y + (block_height/2)
                    text_offset_x = drawing_area / 2
                    svg_document.add(svg_document.text(node.tag,
                                                       insert = ('{0}%'.format(text_offset_x),
                                                                 '{0}%'.format(text_offset_y))
                                                       )
                                     )

            return svg_document
        else:
            raise TypeError('Supplied graph is not of class Tree')