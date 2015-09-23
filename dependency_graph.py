import uuid
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

	def __init__(self, module, db='openerp', server='http://localhost:8069', user='admin', password='admin', upstream=True, downstream=True):
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
			self.downstream_hierarchy = Tree()
			self.upstream_hierarchy = Tree()
			self.downstream_hierarchy.create_node(module, module)
			self.upstream_hierarchy.create_node(module, module)
			if downstream:
				self.get_downstream_hierarchy_for_module(module)
			if upstream:
				self.get_upstream_hierarchy_for_module(module)

	def get_downstream_hierarchy_for_module(self, module, parent=None):
		# Check that module isn't already in hierarchy
		installed = self.module_search(module)
		mod_id = module
		if installed:
			if parent:
				if self.downstream_hierarchy.get_node(module):
					unique_id = uuid.uuid1()
					mod_id = '{0}_{1}'.format(module, unique_id)
				self.downstream_hierarchy.create_node(module, mod_id, parent=parent)
			deps = self.get_downstream_dependencies_for_module(module)
			for mod in deps:
				self.get_downstream_hierarchy_for_module(mod, parent=mod_id)

	def get_upstream_hierarchy_for_module(self, module, parent=None):
		# Check that module isn't already in hierarchy
		installed = self.module_search(module)
		mod_id = module
		if installed:
			mod_tree = Tree()
			print '{0} - {1}'.format(module, parent)
			if parent:
				parent_tree = self.upstream_hierarchy.subtree(parent)
				existing_mod = self.upstream_hierarchy.get_node(module)
				# if existing_mod:
				# 	try:
				# 		unique_id = uuid.uuid1()
				# 		mod_id = '{0}_{1}'.format(module, unique_id)
				# 		mod_tree.create_node(module, mod_id)
				# 		self.upstream_hierarchy.paste(module, parent_tree)
				# 	except ValueError:
				# 		# need to be able to sort out tree properly if issue
				# 		import pdb
				# 		pdb.set_trace()
				# 		print 'meh'
				# else:
				if not existing_mod:
					mod_tree.create_node(module, module)
					mod_tree.paste(module, parent_tree)
					self.upstream_hierarchy = mod_tree
			deps = self.get_upstream_dependencies_for_module(module)
			for mod in deps:
				existing_mod = self.upstream_hierarchy.get_node(mod)
				print '{0} exists: {1}'.format(mod, existing_mod)
				if not existing_mod:
					print '{0} did not exist so getting that'.format(mod)
					self.get_upstream_hierarchy_for_module(mod, parent=mod_id)

	def get_downstream_dependencies_for_module(self, module):
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

	def get_upstream_dependencies_for_module(self, module):
		"""
		Recursively get the modules upstream dependencies
		:param module: The module to get the hierarchy for
		:return: Runs itself again with the new module or returns True
		"""
		mod_id = self.module_search(module)
		if not mod_id:
			return []
		mod_deps = self.module_read(mod_id)
		if not mod_deps:
			return []
		dependent_mod_names = self.upstream_dependency_read(mod_deps['dependencies_id'])
		return dependent_mod_names

	def upstream_dependency_read(self, ids):
		"""
		Read ir.module.module.dependency for the names of the upstream dependencies
		:param ids: ids for the module to get the dependencies
		:return: List of names
		"""
		mods = self.client.read(self.dep_reg, ids, ['name'])
		return [mod['name'] for mod in mods]

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

	def module_read(self, mod_ids):
		"""
		Read ir.module.module and get the dependencies_id for the module
		:param mod_ids:
		:return: List of objects with id, dependencies_id
		"""
		if isinstance(mod_ids, list):
			mod_ids = mod_ids[0]
		return self.client.read(self.mod_reg, mod_ids, ['dependencies_id'])