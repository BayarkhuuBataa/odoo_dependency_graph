from dependency_graph import DependencyGraph
from treelib import Tree


class JsonFormatter:

	def __init__(self, dependency_graph):
		if isinstance(dependency_graph, DependencyGraph):
			self.graph = dependency_graph.hierarchy
		else:
			raise TypeError('Supplied dependency graph is not of class DependencyGraph')

	def convert_hierarchy_to_json(self):
		if isinstance(self.graph, Tree):
			return self.graph.to_json()
		else:
			raise TypeError('Supplied graph is not of class Tree')
