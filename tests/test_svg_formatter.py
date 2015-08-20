__author__ = 'colinwren'

import unittest
from treelib import Tree, Node
from svg_formatter import SvgFormatter
from dependency_graph import DependencyGraph
from mock import Mock
import svgwrite

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
		svgf = SvgFormatter(mock_dp)
		self.assertTrue(hasattr(svgf, 'graph'), 'Init did not set up graph attribute')

	def test_03_raises_error_if_non_tree_graph_passed_to_convert_to_svg(self):
		mock_dp = Mock(spec=DependencyGraph)
		mock_dp.hierarchy = {'test': 'test'}
		svgf = SvgFormatter(mock_dp)
		with self.assertRaises(TypeError):
			svgf.convert_hierarchy_to_svg()

	def test_04_raises_error_if_negative_margin_passed_to_covert_to_svg(self):
		mock_dp = Mock(spec=DependencyGraph)
		mock_dp.hierarchy = self.test_tree
		svgf = SvgFormatter(mock_dp)
		with self.assertRaises(ValueError):
			svgf.convert_hierarchy_to_svg(margin=-666)

	def test_05_creates_a_svg_document_with_name_of_root_node(self):
		mock_dp = Mock(spec=DependencyGraph)
		mock_dp.hierarchy = Tree()
		mock_dp.hierarchy.create_node('test', 'test')
		svgf = SvgFormatter(mock_dp)
		test_svg = svgf.convert_hierarchy_to_svg()
		test_svg_fn = test_svg.filename
		self.assertEqual(test_svg_fn, 'test_dependency_graph.svg', 'Did not create a SVG doc with right height for number of nested dicts - actual = {0}'.format(test_svg_fn))

	def test_06_creates_a_svg_document_with_default_a4_300ppi_size(self):
		mock_dp = Mock(spec=DependencyGraph)
		mock_dp.hierarchy = Tree()
		mock_dp.hierarchy.create_node('test', 'test')
		svgf = SvgFormatter(mock_dp)
		test_svg = svgf.convert_hierarchy_to_svg()
		test_svg_height = test_svg.attribs['height']
		test_svg_width = test_svg.attribs['width']
		self.assertEqual(test_svg_width, '2480px', 'Did not create a SVG doc with right width for a4 300ppi - actual = {0}'.format(test_svg_width))
		self.assertEqual(test_svg_height, '3508px', 'Did not create a SVG doc with right height for a4 300ppi - actual = {0}'.format(test_svg_height))

	def test_07_creates_a_svg_document_with_supplied_size(self):
		mock_dp = Mock(spec=DependencyGraph)
		mock_dp.hierarchy = Tree()
		mock_dp.hierarchy.create_node('test', 'test')
		svgf = SvgFormatter(mock_dp)
		test_svg = svgf.convert_hierarchy_to_svg(width='666px', height='1337px')
		test_svg_height = test_svg.attribs['height']
		test_svg_width = test_svg.attribs['width']
		self.assertEqual(test_svg_width, '666px', 'Did not create a SVG doc with right width for a4 300ppi - actual = {0}'.format(test_svg_width))
		self.assertEqual(test_svg_height, '1337px', 'Did not create a SVG doc with right height for a4 300ppi - actual = {0}'.format(test_svg_height))

	def test_08_creates_a_rect_element_for_each_dependency(self):
		mock_dp = Mock(spec=DependencyGraph)
		mock_dp.hierarchy = self.test_tree
		svgf = SvgFormatter(mock_dp)
		test_svg = svgf.convert_hierarchy_to_svg()
		test_rects_size = [rect for rect in test_svg.elements if isinstance(rect, svgwrite.shapes.Rect)]
		expect_rects_size = self.test_tree.size()
		self.assertEqual(len(test_rects_size), expect_rects_size, 'Did not create a rect element for each dependency - actual = {0}'.format(test_rects_size))

	def test_09_places_the_rect_elements_bottom_up_based_on_depth(self):
		mock_dp = Mock(spec=DependencyGraph)
		mock_dp.hierarchy = self.test_tree
		svgf = SvgFormatter(mock_dp)
		test_svg = svgf.convert_hierarchy_to_svg(width='100px', height='100px', margin=5, padding=1)
		test_rects = [rect for rect in test_svg.elements if isinstance(rect, svgwrite.shapes.Rect)]
		level_0_rect = [r for r in test_rects if r.attribs['class'] == 'level-0'][0]
		level_1_rect = [r for r in test_rects if r.attribs['class'] == 'level-1'][0]
		level_2_rect = [r for r in test_rects if r.attribs['class'] == 'level-2'][0]
		level_3_rect = [r for r in test_rects if r.attribs['class'] == 'level-3'][0]
		level_4_rect = [r for r in test_rects if r.attribs['class'] == 'level-4'][0]
		level_5_rect = [r for r in test_rects if r.attribs['class'] == 'level-5'][0]
		level_6_rect = [r for r in test_rects if r.attribs['class'] == 'level-6'][0]
		self.assertEqual(level_0_rect.attribs['y'], '83%', 'Did not place element correctly')
		self.assertEqual(level_1_rect.attribs['y'], '70%', 'Did not place element correctly')
		self.assertEqual(level_2_rect.attribs['y'], '57%', 'Did not place element correctly')
		self.assertEqual(level_3_rect.attribs['y'], '44%', 'Did not place element correctly')
		self.assertEqual(level_4_rect.attribs['y'], '31%', 'Did not place element correctly')
		self.assertEqual(level_5_rect.attribs['y'], '18%', 'Did not place element correctly')
		self.assertEqual(level_6_rect.attribs['y'], '5%', 'Did not place element correctly')

	def test_10_adds_labels_to_the_rect_elements_with_module_name(self):
		mock_dp = Mock(spec=DependencyGraph)
		mock_dp.hierarchy = Tree()
		mock_dp.hierarchy.create_node('test', 'test')
		svgf = SvgFormatter(mock_dp)
		test_svg = svgf.convert_hierarchy_to_svg(width='100%', height='100%')
		test_texts = [text for text in test_svg.elements if isinstance(text, svgwrite.text.Text)][0]
		self.assertEqual(test_texts.text, 'test', 'Did not add the correct label to the elements')

	# def test_11_when_multiple_nodes_at_depth_each_rect_takes_up_a_percentage_of_row(self):
	# 	# Need to set the x,y, width etc of nodes as set them so can then use this to position children
	# 	self.assertEqual(False, True, 'Test not yet implemented')
	# 	# mock_dp = Mock(spec=DependencyGraph)
	# 	# mock_dp.hierarchy = Tree()
	# 	# mock_dp.hierarchy.create_node('test', 'test')
	# 	# mock_dp.hierarchy.create_node('test_one', 'test_one', parent='test')
	# 	# mock_dp.hierarchy.create_node('test_two', 'test_two', parent='test')
	# 	# svgf = SvgFormatter(mock_dp)
	# 	# test_svg = svgf.convert_hierarchy_to_svg(width='100%', height='100%')
	# 	# test_rects = [rect for rect in test_svg.elements if isinstance(rect, svgwrite.shapes.Rect)]
	# 	# level_1_rect = [r for r in test_rects if r.attribs['class'] == 'level-1'][0]
	# 	# self.assertEqual(level_1_rect.attribs['width'], '44.0%', 'Did not set the correct width for multiple nodes on same depth - actual = {0}'.format(level_1_rect.attribs['width']))