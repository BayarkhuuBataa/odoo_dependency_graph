__author__ = 'colinwren'

import unittest
import erppeek
from mock import MagicMock
from mock import patch
import dependency_graph
from dependency_graph import DependencyGraph

class TestDependencyGraph(unittest.TestCase):

	""" I want this data structure:

	{
		'name': 'odoo_fixes',
		'deps': [
			{
				'name': 'low_level',
				'deps': [
					{
						'name': 'wrapper',
						'deps': [
							{
								'name': 'platform',
								'deps': [
									{
										'name': 'mobile',
										'deps': []
									},
									{
										'name': 'shift_management',
										'deps': [
											{
												'name': 'kamishibai',
												'deps': []
											}
										]
									}
								]
							}
						]
					}
				]
			}
		]
	}

	"""


	@patch('erppeek.Client')
	def test_01_get_erppeek_client_returns_valid_client(self, mock_client):
		"""
		Test that when successfully getting a client get_erppeek_client returns it
		:param mock_client: A mocked out version of erppeek.Client
		:return:
		"""
		test_dp = dependency_graph.get_erppeek_client()
		self.assertEquals(isinstance(test_dp, MagicMock), True, 'Client returned was not an instance of erppeek.Client')
		mock_client.stop()

	@patch('erppeek.Client')
	def test_02_get_erppeek_client_throws_error_if_cant_connect(self, mock_client):
		"""
		Test that when unable to get a client get_erppeek_client raises a RuntimeError
		:param mock_client: a mocked out version of erppeek.Client
		:return:
		"""
		exc = Exception
		mock_client.side_effect = exc
		self.assertRaises(RuntimeError, dependency_graph.get_erppeek_client, 'RuntimeError was not thrown when not being able to connect')
		mock_client.stop()

	@patch('erppeek.Client')
	def test_03_throws_error_when_module_specified_isnt_found_in_db(self, mock_client):
		"""
		Test that when given a module that isn't in the database DependencyGraph will raise a RuntimeError
		:param mock_client: a mocked out version of erppeek.Client
		:return:
		"""
		# Mock Up
		mock_dp = DependencyGraph
		orig_mod_search = mock_dp.module_search
		mock_dp.module_search = MagicMock(return_value=[])

		self.assertRaises(RuntimeError, DependencyGraph, 'RuntimeError was not thrown when not being able to find module in db')

		# Mock Down
		mock_client.stop()
		mock_dp.module_search.stop()
		mock_dp.module_search = orig_mod_search
		mock_client.stop()

	@patch('erppeek.Client')
	def test_04_calls_get_hierarchy_for_module_when_module_is_found_in_db(self, mock_client):
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
		mock_dp.get_hierarchy_for_module.assert_called_with('valid_module', [])

		# Mock Down
		mock_client.stop()
		mock_dp.module_search.stop()
		mock_dp.get_hierarchy_for_module.stop()
		mock_dp.module_search = orig_mod_search
		mock_dp.get_hierarchy_for_module = orig_ghfm

	@patch('erppeek.Client')
	def test_05_get_hierarchy_for_module_returns_false_when_nothing_depend_on_module(self, mock_client):
		"""
		Test that get_hierarchy_for_module returns False if an empty list if returned
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
		test_hierarchy = {'search': [{'name': 'valid_module', 'deps': []}]}
		self.assertEqual(mock_dg.hierarchy, test_hierarchy, 'get_hierarchy_for_module did not return [] when finding no dependent modules')

		# Mock Down
		mock_client.stop()
		mock_dp.module_search.stop()
		mock_client.search.stop()
		mock_client.search = orig_client_search
		mock_dp.dependency_search.stop()
		mock_dp.module_search = orig_mod_search
		mock_dp.dependency_search = orig_dep_search

	@patch('erppeek.Client')
	def test_06_get_hierarchy_for_module_returns_a_nest_dict_when_another_module_depends_on_module(self, mock_client):
		"""
		Test that get_hierarchy_for_module returns a nested dict if another module depends on the module
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
			else:
				return []

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
		test_hierarchy = {'search': [
			{
				'name': 'valid_module',
				'deps': [
					{
						'name': 'dependent_module',
						'deps': []
					}
				]
			}
		]}
		self.assertEqual(mock_dg.hierarchy, test_hierarchy, 'get_hierarchy_for_module did not return nested dict when finding dependent modules')

		# Mock Down
		mock_client.stop()
		mock_dp.module_search.stop()
		mock_client.search.stop()
		mock_client.search = orig_client_search
		mock_dp.dependency_search.stop()
		mock_dp.module_search = orig_mod_search
		mock_dp.dependency_search = orig_dep_search