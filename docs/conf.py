# -*- coding: utf-8 -*-
import sys
import os
import sphinx_rtd_theme
import django


sys.path.insert(0, os.path.abspath("./"))
sys.path.insert(0, os.path.abspath("../"))
sys.path.insert(0, os.path.abspath("../toolkit"))
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
django.setup()

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
]
templates_path = ['_template']
source_suffix = '.rst'
master_doc = 'index'
project = u'CCE Toolkit'
description = u'A collection of python helpers and custom Django views, ' \
              u'forms and models created for rapid development of Management '\
              u'Information Systems'
copyright = u'2016, University of Oklahoma - College of Continuing Education' \
            u' - IT'
author = u'CCE-IT Devs'
version = u'1.1.0'
release = u'1.1.0'
language = 'en'
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = False
html_theme = "sphinx_rtd_theme"
html_favicon = '_static/favicon.ico'
html_static_path = ['_static']
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
htmlhelp_basename = 'CCEToolkitdoc'
latex_elements = {
}
latex_documents = [
    (master_doc, 'CCEToolkit.tex', u'CCE Toolkit Documentation',
     author, 'manual'),
]
man_pages = [
    (master_doc, 'ccetoolkit', u'CCE Toolkit Documentation',
     [author], 1)
]
texinfo_documents = [
    (master_doc, 'CCEToolkit', u'CCE Toolkit Documentation',
     author, 'CCEToolkit', description,
     'Miscellaneous'),
]
