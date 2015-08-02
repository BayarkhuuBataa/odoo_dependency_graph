__author__ = 'colinwren'

import unittest

class TestSvgFormatter(unittest.TestCase):

	def test_01_raises_error_when_initalised_with_non_dependency_graph_class(self):
		self.assertEqual(False, True, 'Did not raise when passed non dependency graph at __init__')

	def test_02_copies_over_hierarchy_when_initialised_with_dependency_graph(self):
		self.assertEqual(False, True, 'Did not copy over hierarchy correctly at __init__')

	def test_03_creates_a_svg_document_with_height_based_on_number_of_nested_dicts(self):
		self.assertEqual(False, True, 'Did not create a SVG doc with right height for number of nested dicts')

	def test_04_creates_a_rect_element_for_each_dependency(self):
		self.assertEqual(False, True, 'Did not create a rect element for each dependency')

	def test_05_places_the_rect_elements_bottom_up_based_on_depth(self):
		self.assertEqual(False, True, 'Did not place the rect elements correctly')

	def test_06_adds_labels_to_the_rect_elements_with_module_name(self):
		self.assertEqual(False, True, 'Did not add the correct label to the elements')

	def test_07_when_a_module_has_multiple_dependencies_the_dependent_module_rects_are_on_the_same_level(self):
		self.assertEqual(False, True, 'Did not put multiple dependencies on the same level')

	def test_08_when_a_dependency_level_has_the_same_module_multiple_times_merge_the_rects(self):
		self.assertEqual(False, True, 'Did not merge the rects when the same module is on the level many times')