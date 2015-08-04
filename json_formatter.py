__author__ = 'colinwren'
from dependency_graph import DependencyGraph

class JsonFormatter:

	def __init__(self, dependency_graph):
		if isinstance(dependency_graph, DependencyGraph):
			self.graph = dependency_graph.hierarchy
		else:
			raise TypeError('Supplied dependency graph is not of class DependencyGraph')

	def convert_hierarchy_to_json(self):
		return self.graph.to_json()
