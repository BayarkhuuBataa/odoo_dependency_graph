__author__ = 'colinwren'

import unittest

class TestDependencyGraph(unittest.TestCase):

	def test_01_get_erppeek_client_returns_valid_client(self):
		self.assertEquals(False, True, 'Client returned was not an instance of erppeek.Client')

	def test_02_get_erppeek_client_throws_error_if_cant_connect(self):
		self.assertEquals(False, True, 'RuntimeError was not thrown when not being able to connect')

	def test_03_throws_error_when_module_specified_isnt_found_in_db(self):
		self.assertEquals(False, True, 'RuntimeError was not thrown when not being able to find module in db')

	def test_04_get_hierarchy_for_module_returns_false_when_nothing_depend_on_module(self):
		self.assertEquals(False, True, 'get_hierarchy_for_module did not return false when finding no dependent modules')

	def test_05_get_hierarchy_for_module_returns_list_of_module_names_when_finding_dependent_modules(self):
		self.assertEquals(False, True, 'get_hierarchy_for_module did not return list of strings when finding dependent modules')