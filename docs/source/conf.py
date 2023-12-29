import os
import sys

# allow autodoc to find the cadscript package
sys.path.insert(0, os.path.abspath('../../'))

project = 'cadscript'
author = 'Andreas Kahler'
source_suffix = ['.rst', '.md']
master_doc = 'index'

html_theme = 'sphinx_rtd_theme'

extensions = [
    'recommonmark',
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',

]

autodoc_default_options = {
    'member-order': 'bysource',
#    'special-members': '__init__',
    'undoc-members': True,
#    'exclude-members': '__weakref__'
}

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

intersphinx_disabled_domains = ['std']