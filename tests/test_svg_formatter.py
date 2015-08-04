__author__ = 'colinwren'

import unittest
from treelib import Tree, Node
from svg_formatter import SvgFormatter
from dependency_graph import DependencyGraph
from mock import Mock

class TestSvgFormatter(unittest.TestCase):

	def setUp(self):
		test_tree = Tree()
		test_tree.create_node('level_one', 'level_one')
		test_tree.create_node('level_two', 'level_two', parent='level_one')
		test_tree.create_node('level_three', 'level_three', parent='level_two')
		test_tree.create_node('level_four_one', 'level_four_one', parent='level_three')
		test_tree.create_node('level_one_five_one', 'level_one_five_one', parent='level_four_one')
		test_tree.create_node('level_one_five_two', 'level_one_five_two', parent='level_four_one')
		test_tree.create_node('level_one_five_two', 'level_one_five_three', parent='level_four_one')
		test_tree.create_node('level_four_two', 'level_four_two', parent='level_three')
		test_tree.create_node('level_two_five', 'level_two_five', parent='level_four_two')
		test_tree.create_node('level_six_one', 'level_six_one', parent='level_two_five')
		test_tree.create_node('level_six_two', 'level_six_two', parent='level_two_five')
		test_tree.create_node('level_six_two', 'level_six_three', parent='level_two_five')
		test_tree.create_node('level_four_three', 'level_four_three', parent='level_three')
		test_tree.create_node('level_three_five_one', 'level_three_five_one', parent='level_four_three')
		test_tree.create_node('level_one_six', 'level_one_six', parent='level_three_five_one')
		test_tree.create_node('level_one_seven_one', 'level_one_seven_one', parent='level_one_six')
		test_tree.create_node('level_one_seven_two', 'level_one_seven_two', parent='level_one_six')
		test_tree.create_node('level_one_seven_three', 'level_one_seven_three', parent='level_one_six')
		test_tree.create_node('level_three_five_two', 'level_three_five_two', parent='level_four_three')
		test_tree.create_node('level_two_six', 'level_two_six', parent='level_three_five_two')
		test_tree.create_node('level_two_seven_one', 'level_two_seven_one', parent='level_two_six')
		test_tree.create_node('level_two_seven_two', 'level_two_seven_two', parent='level_two_six')
		test_tree.create_node('level_two_seven_three', 'level_two_seven_three', parent='level_two_six')
		test_tree.create_node('level_three_five_three', 'level_three_five_three', parent='level_four_three')
		test_tree.create_node('level_three_six', 'level_three_six', parent='level_three_five_three')
		test_tree.create_node('level_three_seven_one', 'level_three_seven_one', parent='level_three_six')
		test_tree.create_node('level_three_seven_two', 'level_three_seven_two', parent='level_three_six')
		test_tree.create_node('level_three_seven_three', 'level_three_seven_three', parent='level_three_six')
		test_tree.create_node('level_three_five_four', 'level_three_five_four', parent='level_four_three')
		test_tree.create_node('level_four_six', 'level_four_six', parent='level_three_five_four')
		test_tree.create_node('level_four_seven_one', 'level_four_seven_one', parent='level_four_six')
		test_tree.create_node('level_four_seven_two', 'level_four_seven_two', parent='level_four_six')
		test_tree.create_node('level_four_seven_three', 'level_four_seven_three', parent='level_four_six')
		self.test_tree = test_tree

	def test_01_raises_error_when_initalised_with_non_dependency_graph_class(self):
		self.assertRaises(TypeError, SvgFormatter, 'Init did not catch non dependency graph class')

	def test_02_initialises_with_dependency_graph_object(self):
		mock_dp = Mock(spec=DependencyGraph)
		mock_dp.hierarchy = Tree()
		mock_dp.hierarchy.create_node('test', 'test')
		jsonf = SvgFormatter(mock_dp)
		self.assertTrue(hasattr(jsonf, 'graph'), 'Init did not set up graph attribute')

	def test_03_raises_error_if_non_tree_graph_passed_to_convert_to_json(self):
		mock_dp = Mock(spec=DependencyGraph)
		mock_dp.hierarchy = {'test': 'test'}
		jsonf = SvgFormatter(mock_dp)
		with self.assertRaises(TypeError):
			jsonf.convert_hierarchy_to_svg()

	def test_04_creates_a_svg_document_with_height_based_on_number_of_nested_dicts(self):
		self.assertEqual(False, True, 'Did not create a SVG doc with right height for number of nested dicts')

	def test_05_creates_a_rect_element_for_each_dependency(self):
		self.assertEqual(False, True, 'Did not create a rect element for each dependency')

	def test_06_places_the_rect_elements_bottom_up_based_on_depth(self):
		self.assertEqual(False, True, 'Did not place the rect elements correctly')

	def test_07_adds_labels_to_the_rect_elements_with_module_name(self):
		self.assertEqual(False, True, 'Did not add the correct label to the elements')

	def test_08_when_a_module_has_multiple_dependencies_the_dependent_module_rects_are_on_the_same_level(self):
		self.assertEqual(False, True, 'Did not put multiple dependencies on the same level')

	def test_09_when_a_dependency_level_has_the_same_module_multiple_times_merge_the_rects(self):
		self.assertEqual(False, True, 'Did not merge the rects when the same module is on the level many times')