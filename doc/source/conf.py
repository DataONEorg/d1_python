
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

project = "DataONE Python Products"
copyright = "2019 Participating institutions in DataONE"

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
]
pygments_style = "sphinx"
today_fmt = "%Y-%m-%d"

extensions = [
    # 'sphinx.ext.pngmath',
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.graphviz",
    "sphinx.ext.ifconfig",
    "sphinx.ext.imgmath",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
]

# The default syntax highlighting applied code-block and :: blocks
highlight_language = "bash"

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

napoleon_use_param = False
napoleon_use_ivar = True
napoleon_include_init_with_doc = True

# Autodoc

autodoc_member_order = "bysource"

autodoc_default_flags = [
    # Include regular members.
    "members",
    # "show-inheritance",
    # Include members without docstrings.
    # "undoc-members",
    # Include members
    # "private-members",
    # "special-members",
    # "inherited-members",
]

EXCLUDED_MEMBERS_LIST = (
    # special-members
    "__weakref__",
    "__doc__",
    "__module__",
    # undoc-members
    "__dict__",
)


def autodoc_skip_member(app, what, name, obj, skip, options):
    exclude = name in EXCLUDED_MEMBERS_LIST
    return skip or exclude


def setup(app):
    sys.path.insert(0, os.path.abspath('../../lib_common/src/'))
    sys.path.insert(0, os.path.abspath('../../lib_client/src/'))
    sys.path.insert(0, os.path.abspath('../../test_utilities/src/'))
    sys.path.insert(0, os.path.abspath('../../dev_tools/src/'))

    app.connect("autodoc-skip-member", autodoc_skip_member)
