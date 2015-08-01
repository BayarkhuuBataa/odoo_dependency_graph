__author__ = 'colinwren'

from dependency_graph import DependencyGraph
from json_formatter import JsonFormatter
import unittest
from mock import Mock
import json

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
		mock_dp.hierarchy = {'search': [
			{
				'name': 'level_one',
				'deps': [
					{
						'name': 'level_two_one',
						'deps': [
							{
								'name': 'level_three',
								'deps': []
							}
						]
					},
					{
						'name': 'level_two_two',
						'deps': []
					}
				]
			}
		]}
		jsonf = JsonFormatter(mock_dp)
		self.assertEqual(json.loads(jsonf.convert_hierarchy_to_json()), mock_dp.hierarchy, 'JSON not formatted correclty')
