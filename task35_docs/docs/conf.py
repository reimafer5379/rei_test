# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath('/home/rei_f/inf/python_app/task5'))

project = "Light 'em up!"
copyright = '2026, REI_F'
author = 'REI_F'
release = '1.0'
version = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.napoleon',
              'sphinx.ext.viewcode',
              'sphinx.ext.todo',
              'sphinx.ext.intersphinx',
              'sphinx.ext.coverage'
              ]

exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    '**/__pycache__',
]
templates_path = ['_templates']

autodoc_typehints = 'description'
autodoc_member_order = 'bysource'
autodoc_default_options = {
    'members': True,
    'undoc-members': False,
    'private-members': False,
    'special-members': '__init__',
    'inherited-members': False,
    'show-inheritance': True,
}

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True




# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
html_title = f"{project} Documentation"
html_short_title = "Puzzle Game Docs"

todo_include_todos = True
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}
