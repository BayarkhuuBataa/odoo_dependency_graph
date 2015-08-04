__author__ = 'colinwren'

import erppeek
from treelib import Tree


def get_erppeek_client(server='http://localhost:8069', db='openerp', user='admin', password='admin'):
	"""
	Get a ERPPeek client for us to use, if one not available then close the function
	:param server: Server address (with XML-RPC port)
	:param db: Name of database
	:param user: Username to connect with
	:param password: Password for username connecting with
	:return: A erppeek.Client object we can use for XML-RPC calls
	"""
	try:
		client = erppeek.Client(server, db=db, user=user, password=password, verbose=False)
	except:
		raise RuntimeError("Error connecting to {0} on {1} using credentials {2}:{3}".format(db, server, user, password))
	return client


class DependencyGraph:

	def __init__(self, module, db='openerp', server='http://localhost:8069', user='admin', password='admin'):
		"""
		Get a ERPPeek client, check the module we want to generate the graph for is in the database and generate the
		hierarchy ready for formatting
		:param module: Name of the module we want to generate the hierarchy for
		:param db: Database to generate the hierarchy from
		:param server: Odoo server address
		:param user: Username - defaults to admin so we can access info on modules
		:param password: Password for user we're connecting as
		:return: An hierarchy object for the module specified
		"""
		self.client = get_erppeek_client(server=server, db=db, user=user, password=password)
		self.mod_reg = 'ir.module.module'
		self.dep_reg = 'ir.module.module.dependency'
		# check that the module in question exists
		module_present = self.module_search(module)
		if not module_present:
			raise RuntimeError("{m} module not found in database".format(m=module))
		else:
			self.hierarchy = Tree()
			self.hierarchy.create_node(module, module)
			self.get_hierarchy_for_module(module)

	def get_hierarchy_for_module(self, module, parent=None):
		# Check that module isn't already in hierarchy
		installed = self.module_search(module)
		if installed:
			if parent:
				try:
					self.hierarchy.create_node(module, module, parent=parent)
				except:
					pass
			deps = self.get_dependencies_for_module(module)
			for mod in deps:
				self.get_hierarchy_for_module(mod, parent=module)

	def get_dependencies_for_module(self, module):
		"""
		Recursively get the hierarchy for a module
		:param module: The module to get the hierarchy for
		:return: Runs itself again with the new module or returns True
		"""
		# Search for modules that depend on the module
		dependent_mod_ids = self.dependency_search(module)
		if not dependent_mod_ids:
			return []
		dependent_mod_names = self.dependency_read(dependent_mod_ids)
		return dependent_mod_names

	def dependency_read(self, ids):
		"""
		Read ir.module.module.dependency for the names of the modules with the supplied IDs
		:param ids: List of IDs for modules supplied
		:return: List of names
		"""
		deps = self.client.read(self.dep_reg, ids, ['module_id'])
		mod_ids = [dep['module_id'][0] for dep in deps]
		mods = self.client.read(self.mod_reg, mod_ids, ['name'])
		return [mod['name'] for mod in mods]

	def dependency_search(self, module):
		"""
		Search ir.module.module.dependency for the IDs of modules that depend on the module
		:param module: Name of the module to look for depending modules
		:return: List of IDs
		"""
		return self.client.search(self.dep_reg, [['state', '=', 'installed'], ['name', '=', module]])

	def module_search(self, module):
		"""
		Search ir.module.module for the IDs of module
		:param module: Name of the module to look for
		:return: List of IDs
		"""
		return self.client.search(self.mod_reg, [['state', '=', 'installed'], ['name', '=', module]])
