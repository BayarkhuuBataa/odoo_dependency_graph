__author__ = 'colinwren'

import erppeek


def get_erppeek_client(server='http://localhost:8069', db='openerp', user='admin', password='admin'):
	"""
	Get a ERPPeek client for us to use, if one not available then close the function
	:param server: Server address (with XML-RPC port)
	:param db: Name of database
	:param user: Username to connect with
	:param password: Password for username connecting with
	:return: A erppeek.Client object we can use for XML-RPC calls
	"""
	client = None
	try:
		client = erppeek.Client(server, db=db, user=user, password=password, verbose=False)
	except:
		raise RuntimeError("Error connecting to {d} on {s} using credentials {u}:{p}".format(d=db, s=server, u=user, p=password))
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
			self.hierarchy = self.get_hierarchy_for_module(module)

	def get_hierarchy_for_module(self, module):
		"""
		Recursively get the hierarchy for a module
		:param module: The module to get the hierarchy for
		:return: Runs itself again with the new module or returns True
		"""
		# Search for modules that depend on the module
		dependent_mod_ids = self.dependency_search(module)
		if not dependent_mod_ids:
			return False

	def dependency_search(self, module):
		return self.client.search(self.dep_reg, [['name', '=', module]])

	def module_search(self, module):
		return self.client.search(self.mod_reg, [['name', '=', module]])