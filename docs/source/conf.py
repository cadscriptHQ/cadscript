import os
import sys

# allow autodoc to find the cadscript package and extensions
sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../'))

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
    'sphinx.ext.viewcode',
    'ext.cadscript_directives',
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

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

