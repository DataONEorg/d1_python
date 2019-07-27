# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Sphinx configuration for DataONE Python Products documentation."""
import os
import sys

import better
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'd1_gmn.settings'
django.setup()

project = "DataONE Python Products"
copyright = "2019 Participating institutions in DataONE"

import d1_gmn.app.models

source_suffix = ".rst"
master_doc = "index"
version = ""
release = ""

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "tests",
    "test*.py",
    "subject_info_renderer.py",
    '*/generated/*',
]

pygments_style = "sphinx"
today_fmt = "%Y-%m-%d"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.graphviz",
    "sphinx.ext.ifconfig",
    "sphinx.ext.imgmath",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.napoleon",
    # 'sphinxcontrib.napoleon',
    "sphinx.ext.todo",
]

# The default syntax highlighting applied code-block and :: blocks.
# Set highlighting where needed, e.g., with ".. highlight:: python".
highlight_language = "none"

html_logo = "_static/dataone_logo.png"
html_theme_path = [better.better_theme_path]
html_theme = "better"
html_short_title = "Home"

html_static_path = ["_static"]

templates_path = ["_templates"]

html_theme_options = {
    # show sidebar on the right instead of on the left
    "rightsidebar": False,
    # inline CSS to insert into the page if you're too lazy to make a
    # separate file
    "inlinecss": "",
    # CSS files to include after all other CSS files
    # (refer to by relative path from conf.py directory, or link to a
    # remote file)
    "cssfiles": [],
    # show a big text header with the value of html_title
    "showheader": True,
    # show the breadcrumbs and index|next|previous links at the top of
    # the page
    "showrelbartop": True,
    # same for bottom of the page
    "showrelbarbottom": False,
    # show the self-serving link in the footer
    "linktotheme": True,
    # width of the sidebar. page width is determined by a CSS rule.
    # I prefer to define things in rem because it scales with the
    # global font size rather than pixels or the local font size.
    "sidebarwidth": "15rem",
    # color of all body text
    "textcolor": "#000000",
    # color of all headings (<h1> tags); defaults to the value of
    # textcolor, which is why it's defined here at all.
    "headtextcolor": "",
    # color of text in the footer, including links; defaults to the
    # value of textcolor
    "footertextcolor": "",
    # Google Analytics info
    "ga_ua": "",
    "ga_domain": "",
}

# html_sidebars = {
#   '**': ['localtoc.html', 'sourcelink.html', 'searchbox.html'],
# }

# Formatting of NumPy and Google style docstrings

# Toggled Napoleon switches
napoleon_use_param = False
napoleon_use_ivar = True
napoleon_include_init_with_doc = True
# Napoleon settings
# napoleon_google_docstring = True
# napoleon_numpy_docstring = True
# napoleon_include_private_with_doc = False
# napoleon_include_special_with_doc = False
# napoleon_use_admonition_for_examples = False
# napoleon_use_admonition_for_notes = False
# napoleon_use_admonition_for_references = False
# napoleon_use_rtype = True
# napoleon_use_keyword = True
# napoleon_custom_sections = None

# Autodoc

autodoc_default_options = {
    # 'members': None,
    'member-order': 'bysource',
    'special-members': ','.join(('__init__',)),
    'exclude-members': ','.join((
        "__weakref__", "__doc__", "__module__", "__dict__",
    )),
    # Members starting with underscore are excluded by default. This specifies
    # exceptions, which will be included.
    # Don't show the base classes for the class.
    'show-inheritance': False,
    # Ignore members imported by __all__().
    # 'ignore-module-all': True,
    # Prevent imported and inherited members from being documented as part of the
    # classes they're imported/inherited in. They still get documented as separate
    # classes.
    'imported-members': False,
    ########
    'inherited-members': True,
    # Skip private members.
    # 'private-members': False,
    # Skip members without docstrings.
    # 'undoc-members': False,
}

# Create unique labels for autogenerated modules by prefixing with the path of the
# module.
autosectionlabel_prefix_document = True

# Combine the doc for the class and for __init__ and render it in the
# class.
autoclass_content = 'both'

def autodoc_skip_member(app, what, name, obj, skip, options):
    """Skip members matching criteria"""
    exclude_member = name in [
        'NAMES_2K',
        'UNICODE_NAMES',
        'UNICODE_TEST_STRINGS',
        'WORDS_1K',
        'models.py',
    ]
    exclude_obj = obj is [
        d1_gmn.app.models.ResourceMap
    ]
    if exclude_obj:
        sys.exit(obj)
    exclude = exclude_member or exclude_obj
    return skip or exclude

def autodoc_process_signature(app, what, name, obj, options, signature,
                              return_annotation):
    # print(app, what, name, obj, options, signature, return_annotation)
    pass


def setup(app):
    for pkg_root in (
            'client_cli',
            'client_onedrive',
            'csw',
            'dev_tools',
            'gmn',
            'lib_client',
            'lib_common',
            'lib_scimeta',
            'test_utilities',
            'utilities',
    ):
        sys.path.insert(0, os.path.abspath(f"../../{pkg_root}/src/"))

    app.connect("autodoc-skip-member", autodoc_skip_member)
    # app.connect("autodoc-process-signature", autodoc_process_signature)
