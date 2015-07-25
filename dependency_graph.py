__author__ = 'colinwren'

import erppeek


class DependencyGraph:

	@staticmethod
	def get_erppeek_client(server='http://localhost:8069', db='openerp', user=None, password=None, verbose=False):
		client = None
		try:
			client = erppeek.Client(server, db=db, user=user, password=password, verbose=verbose)
		except:
			print "Error connecting to {d} on {s} using credentials {u}:{p}".format(d=db, s=server, u=user, p=password)
			print "Exiting...."
			exit(1)
		return client

	def __init__(self, module, db='openerp', server='http://localhost:8069', user=None, password=None, verbose=False):
		self.client = self.get_erppeek_client(server=server, db=db, user=user, password=password, verbose=verbose)
		self.hierarchy = self.get_hierarchy_for_module(module)

	def get_hierarchy_for_module(self, module):
		mod_reg = 'ir.module.module'
		dep_reg = 'ir.module.module.dependency'
		# Check the module in question exists
		module_present = self.client.search(mod_reg, [['name', '=', module]])
		if not module_present:
			print "{m} module not found in database".format(m=module)
			exit(1)
		# Generate the tree from the module
		return True