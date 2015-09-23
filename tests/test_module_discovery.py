__author__ = 'colinwren'

import unittest

from treelib import Tree
from mock import MagicMock
from mock import patch
from dependency_graph.dependency_graph import DependencyGraph


class TestModuleDiscovery(unittest.TestCase):

	@patch('erppeek.Client')
	def test_01_calls_get_hierarchy_for_module_when_module_is_found_in_db(self, mock_client):
		"""
		Test that on being passed a valid module the script will go on to call get_hierarchy_for_module
		:param mock_client: a mocked out version of erppeek.Client
		:return:
		"""
		# Mock Up
		mock_dp = DependencyGraph
		orig_mod_search = mock_dp.module_search
		orig_ghfm = mock_dp.get_hierarchy_for_module
		mock_dp.module_search = MagicMock(return_value=[666])
		mock_dp.get_hierarchy_for_module = MagicMock()

		mock_dp('valid_module')
		mock_dp.get_hierarchy_for_module.assert_called_with('valid_module')

		# Mock Down
		mock_client.stop()
		mock_dp.module_search.stop()
		mock_dp.get_hierarchy_for_module.stop()
		mock_dp.module_search = orig_mod_search
		mock_dp.get_hierarchy_for_module = orig_ghfm

	@patch('erppeek.Client')
	def test_02_get_hierarchy_for_module_returns_single_node_when_nothing_depend_on_module(self, mock_client):
		"""
		Test that get_hierarchy_for_module returns a single node tree structure if no dependent modules are found
		:param mock_client: A mocked out version of erppeek.Client
		:return:
		"""
		# Mock Up
		mock_dp = DependencyGraph
		orig_mod_search = mock_dp.module_search
		orig_dep_search = mock_dp.dependency_search
		orig_client_search = mock_client.search
		mock_dp.module_search = MagicMock(return_value=[666])
		mock_dp.dependency_search = MagicMock(return_value=[])

		mock_dg = mock_dp('valid_module')
		test_hierarchy = Tree()
		test_hierarchy.create_node('valid_module', 'valid_module')
		self.assertEqual(mock_dg.hierarchy.to_json(), test_hierarchy.to_json(), 'get_hierarchy_for_module did not return [] when finding no dependent modules')

		# Mock Down
		mock_client.stop()
		mock_dp.module_search.stop()
		mock_client.search.stop()
		mock_client.search = orig_client_search
		mock_dp.dependency_search.stop()
		mock_dp.module_search = orig_mod_search
		mock_dp.dependency_search = orig_dep_search

	@patch('erppeek.Client')
	def test_03_get_hierarchy_for_module_returns_a_two_node_tree_when_another_module_depends_on_module(self, mock_client):
		"""
		Test that get_hierarchy_for_module returns a tree structure with two nodes if a dependent module is found
		:param mock_client: A mocked out version of erppeek.Client
		:return:
		"""
		# Mock Up
		mock_dp = DependencyGraph
		orig_mod_search = mock_dp.module_search
		orig_dep_search = mock_dp.dependency_search
		orig_client_search = mock_client.search
		mock_dp.module_search = MagicMock(return_value=[666])

		def dependency_search_side_effect(value):
			if value == 'valid_module':
				return [666]
			elif value == 'dependent_module':
				return [668]

		mock_dp.dependency_search = MagicMock()
		mock_dp.dependency_search.side_effect = dependency_search_side_effect

		def dependency_read_side_effect(value):
			if value == [666]:
				return ['dependent_module']
			else:
				return []

		mock_dp.dependency_read = MagicMock()
		mock_dp.dependency_read.side_effect = dependency_read_side_effect

		mock_dg = mock_dp('valid_module')
		test_hierarchy = Tree()
		test_hierarchy.create_node('valid_module', 'valid_module')
		test_hierarchy.create_node('dependent_module', 'dependent_module', parent='valid_module')
		self.assertEqual(mock_dg.hierarchy.to_json(), test_hierarchy.to_json(), 'get_hierarchy_for_module did not return nested dict when finding dependent modules')

		# Mock Down
		mock_client.stop()
		mock_dp.module_search.stop()
		mock_client.search.stop()
		mock_client.search = orig_client_search
		mock_dp.dependency_search.stop()
		mock_dp.module_search = orig_mod_search
		mock_dp.dependency_search = orig_dep_search

	@patch('erppeek.Client')
	def test_04_get_hierarchy_renames_duplicate_modules(self, mock_client):
		"""
		Test that get_hierarchy_for_module renames the second instance of a dependent modules ID so can list that module multiple times
		- valid_module
		  - dependent_module_one
		  - dependent_module_two
		    - dependent_mdodule_one1

		:param mock_client: A mocked out version of erppeek.Client
		:return:
		"""
		# Mock Up
		mock_dp = DependencyGraph
		orig_mod_search = mock_dp.module_search
		orig_dep_search = mock_dp.dependency_search
		orig_client_search = mock_client.search
		mock_dp.module_search = MagicMock(return_value=[666])

		def dependency_search_side_effect(value):
			if value == 'valid_module':
				return [666]
			elif value == 'dependent_module_one':
				return [668]
			elif value == 'dependent_module_two':
				return [664]

		mock_dp.dependency_search = MagicMock()
		mock_dp.dependency_search.side_effect = dependency_search_side_effect

		def dependency_read_side_effect(value):
			if value == [666]:
				return ['dependent_module_one', 'dependent_module_two']
			elif value == [664]:
				return ['dependent_module_one']
			else:
				return []

		mock_dp.dependency_read = MagicMock()
		mock_dp.dependency_read.side_effect = dependency_read_side_effect

		mock_dg = mock_dp('valid_module')
		test_hierarchy = Tree()
		test_hierarchy.create_node('valid_module', 'valid_module')
		test_hierarchy.create_node('dependent_module_one', 'dependent_module_one', parent='valid_module')
		test_hierarchy.create_node('dependent_module_two', 'dependent_module_two', parent='valid_module')
		test_hierarchy.create_node('dependent_module_one', 'dependent_module_one1', parent='dependent_module_two')
		self.assertEqual(mock_dg.hierarchy.to_json(), test_hierarchy.to_json(), 'get_hierarchy_for_module did not return nested dict when finding dependent modules')

		# Mock Down
		mock_client.stop()
		mock_dp.module_search.stop()
		mock_client.search.stop()
		mock_client.search = orig_client_search
		mock_dp.dependency_search.stop()
		mock_dp.module_search = orig_mod_search
		mock_dp.dependency_search = orig_dep_search