from setuptools import setup

setup(
    name="odoo_dependency_graph",
    version="0.1",
    description="A tool for showing dependency trees for modules installed on an Odoo instance",
    author="Colin Wren",
    author_email="colin@gimpneek.com",
    url="http://github.com/Gimpneek/odoo_dependency_graph",
    provides=["odoo_dependency_graph"],
    packages=['dependency_graph'],
    entry_points={
        "console_scripts": [
            "odoo_dependency_graph = dependency_graph.__main__:main"
        ],
    },
    install_requires=['ERPPeek>=1.6.1', 'treelib>=1.3.1', 'svgwrite>=1.1.6', 'argparse>=1.4.0'],
    license="GPL",
    zip_safe=True,
)
