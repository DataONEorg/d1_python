# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
"""Sphinx configuration for DataONE Python Products documentation
"""

import sys
import os

import better


project = u'DataONE Python Products'
copyright = u'2016 Participating institutions in DataONE'

source_suffix = '.rst'
master_doc = 'index'
version = ''
release = ''
exclude_trees = ['_build', '_templates']
pygments_style = 'sphinx'
today_fmt = '%Y-%m-%d'

extensions = [
  'sphinx.ext.autodoc',
  'sphinx.ext.doctest',
  'sphinx.ext.todo',
  'sphinx.ext.graphviz',
  'sphinx.ext.autosummary',
  #'sphinx.ext.imgmath',
  'sphinx.ext.pngmath',
  'sphinx.ext.ifconfig',
  'sphinx.ext.inheritance_diagram',
  'sphinx.ext.extlinks',
]

html_logo = 'dataone_logo.png'
html_theme_path = [better.better_theme_path]
html_theme = 'better'
html_short_title = "Home"

html_theme_options = {
  # show sidebar on the right instead of on the left
  'rightsidebar': False,

  # inline CSS to insert into the page if you're too lazy to make a
  # separate file
  'inlinecss': '',

  # CSS files to include after all other CSS files
  # (refer to by relative path from conf.py directory, or link to a
  # remote file)
  'cssfiles': [],  # default is empty list

  # show a big text header with the value of html_title
  'showheader': True,

  # show the breadcrumbs and index|next|previous links at the top of
  # the page
  'showrelbartop': True,
  # same for bottom of the page
  'showrelbarbottom': False,

  # show the self-serving link in the footer
  'linktotheme': True,

  # width of the sidebar. page width is determined by a CSS rule.
  # I prefer to define things in rem because it scales with the
  # global font size rather than pixels or the local font size.
  'sidebarwidth': '15rem',

  # color of all body text
  'textcolor': '#000000',

  # color of all headings (<h1> tags); defaults to the value of
  # textcolor, which is why it's defined here at all.
  'headtextcolor': '',

  # color of text in the footer, including links; defaults to the
  # value of textcolor
  'footertextcolor': '',

  # Google Analytics info
  'ga_ua': '',
  'ga_domain': '',
}

# html_sidebars = {
#   '**': ['localtoc.html', 'sourcelink.html', 'searchbox.html'],
# }
