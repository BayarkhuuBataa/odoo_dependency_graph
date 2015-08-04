__author__ = 'colinwren'

from dependency_graph import DependencyGraph
from json_formatter import JsonFormatter
import unittest
from mock import Mock
from treelib import Tree

class TestJsonFormatter(unittest.TestCase):

	def test_01_raises_error_if_non_dependency_graph_object_passed(self):
		self.assertRaises(TypeError, JsonFormatter, 'Init did not catch non dependency graph class')

	def test_02_initialises_with_dependency_graph_object(self):
		mock_dp = Mock(spec=DependencyGraph)
		mock_dp.hierarchy = {'search': []}
		jsonf = JsonFormatter(mock_dp)
		self.assertTrue(hasattr(jsonf, 'graph'), 'Init did not set up graph attribute')

	def test_03_convert_to_json_returns_string_of_hierarchy(self):
		mock_dp = Mock(spec=DependencyGraph)
		mock_dp.hierarchy = Tree()
		mock_dp.hierarchy.create_node('level_one', 'level_one')
		mock_dp.hierarchy.create_node('level_two_one', 'level_two_one', parent='level_one')
		mock_dp.hierarchy.create_node('level_two_two', 'level_two_two', parent='level_one')
		mock_dp.hierarchy.create_node('level_three', 'level_three', parent='level_two_one')
		jsonf = JsonFormatter(mock_dp)
		self.assertEqual(jsonf.convert_hierarchy_to_json(), mock_dp.hierarchy.to_json(), 'JSON not formatted correclty')
