# Odoo Dependency Graph Generator
A simple script that creates a dependency graph for a given Odoo module. 

## How it does it
The script fires up ERPPeek and using the ir.module.module & ir.module.module.dependencies models creates a hierarchy
graph which can exported via terminal, SVG or JSON. 
