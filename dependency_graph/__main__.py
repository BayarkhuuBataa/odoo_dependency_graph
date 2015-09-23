from dependency_graph import DependencyGraph
import argparse
import sys

parser = argparse.ArgumentParser('Generate a dependency tree for a module installed in an Odoo instance')
parser.add_argument('module', type=str, help='Name of module to get dependency graph tree')
parser.add_argument('--server', type=str,
                    help='Absolute server address for Odoo instance (default: http://localhost:8069)',
                    default='http://localhost:8069')
parser.add_argument('--db', type=str,
                    help='Name of database on Odoo instance (default: openerp)',
                    default='openerp')
parser.add_argument('--user', type=str,
                    help='Username of admin user on Odoo instance (default: admin)',
                    default='admin')
parser.add_argument('--password', type=str,
                    help='Password for admin on Odoo instance (default: admin)',
                    default='admin')


def main():
    args = parser.parse_args()
    dep_graph = DependencyGraph(args.module, db=args.db, server=args.server, user=args.user, password=args.password)
    print dep_graph.hierarchy.show()

if __name__ == '__main__':
    sys.exit(main())
