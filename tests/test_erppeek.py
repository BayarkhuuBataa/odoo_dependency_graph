__author__ = 'colinwren'

import unittest
from mock import MagicMock
from mock import patch
import dependency_graph
from dependency_graph import DependencyGraph

class TestErppeekHandling(unittest.TestCase):

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