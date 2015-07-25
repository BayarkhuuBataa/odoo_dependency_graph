__author__ = 'colinwren'

import unittest
import erppeek
from mock import MagicMock
from mock import patch
import dependency_graph
from dependency_graph import DependencyGraph

class TestDependencyGraph(unittest.TestCase):

	@patch('erppeek.Client')
	def test_01_get_erppeek_client_returns_valid_client(self, mock_client):
		test_dp = dependency_graph.get_erppeek_client()
		self.assertEquals(isinstance(test_dp, MagicMock), True, 'Client returned was not an instance of erppeek.Client')

	@patch('erppeek.Client')
	def test_02_get_erppeek_client_throws_error_if_cant_connect(self, mock_client):
		exc = Exception
		mock_client.side_effect = exc
		self.assertRaises(RuntimeError, dependency_graph.get_erppeek_client, 'RuntimeError was not thrown when not being able to connect')

	@patch('erppeek.Client')
	def test_03_throws_error_when_module_specified_isnt_found_in_db(self, mock_client):
		mock_dp = DependencyGraph
		mock_dp.module_search = MagicMock(return_value=[])
		self.assertRaises(RuntimeError, DependencyGraph, 'RuntimeError was not thrown when not being able to find module in db')

	@patch('erppeek.Client')
	def test_04_calls_get_hierarchy_for_module_when_module_is_found_in_db(self, mock_client):
		mock_dp = DependencyGraph
		mock_dp.module_search = MagicMock(return_value=[666])
		mock_dp.get_hierarchy_for_module = MagicMock()
		mock_dp('valid_module')
		mock_dp.get_hierarchy_for_module.assert_called_with('valid_module')

	# @patch('erppeek.Client')
	# def test_05_get_hierarchy_for_module_returns_false_when_nothing_depend_on_module(self, mock_client):
	# 	mock_dp = DependencyGraph
	# 	mock_dp.module_search = MagicMock(return_value=[666])
	# 	mock
	# 	self.assertEquals(False, True, 'get_hierarchy_for_module did not return false when finding no dependent modules')
	#
	# def test_06_get_hierarchy_for_module_returns_list_of_module_names_when_finding_dependent_modules(self):
	# 	self.assertEquals(False, True, 'get_hierarchy_for_module did not return list of strings when finding dependent modules')