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

"""Generate a text document that contains a normalized representation of an XML
document.

For unit testing, we want to be able to store and compare samples representing XML
documents that are guaranteed to be stable.

Often, XML docs have various sections containing unordered sets of elements, such as
list of subjects, where there are no semantics associated with the order in which they
appear in the doc. The same is true for element attributes.

Since the source for such elements are often dict and set based containers that
themselves don't provide deterministic ordering, serializing a group of such objects can
generate a large number of possible XML docs that, while semantically identical, cannot
be directly compared as text or in the DOM.

Normalizing the formatting can be done with a single deserialize to DOM and back to XML,
but that will not normalize the ordering of the elements, Without a schema, automated
tools cannot rearrange elements in an XML doc, since it is not known if the order is
significant. However, for generating and comparing XML doc samples, a stable document
that contains all the information from the XML doc is sufficient.

The strategy for generating a stable representation of an XML doc is as follows:

- All sibling XML elements must be sorted regardless of where they are in the tree.

- Each element is the root of a branch of the node tree. Sorting, of course, is based on
comparing individual elements in order to determine their relative orderings. If the
information in the elements themselves is identical, it is necessary to break the tie by
recursively comparing their descendants until either a difference is found, or the two
elements are determined to be the roots of two identical branches.

- To enable the sort algorithm to compare the branches, sort keys that hold all
information in the branch are generated and passed to the sort. For comparisons to
properly compare elements in the most to least significant order, each node in the
branch must be in a single list item. So the key is a nested list of lists.

- Finally, since the sort keys are generated from the descendants, siblings in a given
element can only be sorted after all their descendants in the tree have been sorted. So
the tree must be traversed depth first, and the sort performed as the algorithm is
stepping up from a completed level.

- To avoid having to build a new tree depth first, inline sort is used.
"""
import io

import d1_common.date_time
import d1_common.type_conversions


def get_normalized_xml_representation(xml):
    """Return a str that contains a normalized representation of an XML
    document."""
    etree = d1_common.type_conversions.str_to_etree(xml)
    stable_tree = etree_to_stable_tree(etree)
    stable_tree.sortme()
    return stable_tree


def etree_to_stable_tree(t, e=None):
    """Convert an ElementTree to a StableTree:

    - Node attributes become @key:string in the parent dict
    - Text elements become @text:string
    - name is the name of the xml element
    - dict contains the direct children of the element
    - list contains a list of dict
    """
    tag = d1_common.type_conversions.replace_namespace_with_prefix(t.tag)
    e = e or StableNode(tag)
    if t.attrib:
        for k, v in t.attrib.items():
            e.add_child(
                StableNode(
                    "@" + d1_common.type_conversions.replace_namespace_with_prefix(k), v
                )
            )
    if t.text and t.text.strip() != "":
        e.add_child(StableNode("#text", t.text.strip()))
    for child in list(t):
        e.add_child(etree_to_stable_tree(child))
    return e


class StableNode:
    """Tree structure that uses lists instead of dicts, as lists have
    deterministic ordering."""

    def __init__(self, name, child_node=None):
        """child is E or str."""
        self.name = name
        self.child_list = []
        if child_node is not None:
            self.add_child(child_node)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = io.StringIO()
        self.get_str(s, 0)
        return s.getvalue()

    @property
    def text_nodes(self):
        return [n for n in self.child_list if isinstance(n, str)]

    @property
    def element_nodes(self):
        return [n for n in self.child_list if not isinstance(n, str)]

    @property
    def is_text_node(self):
        return len(self.child_list) == 1 and isinstance(self.child_list[0], str)

    @property
    def have_multiple_text_nodes(self):
        return len(self.text_nodes) > 1

    @property
    def have_multiple_element_nodes(self):
        return len(self.element_nodes) > 1

    def add_child(self, e):
        self.child_list.append(e)

    def get_str(self, s, indent):
        self.iwrite(s, indent, "{} = [".format(self.name))
        # self.iwrite(s, indent, 'key = "{}"'.format(self.get_sort_key()))
        for c in self.child_list:
            if c.is_text_node:
                if c.name == "#text":
                    self.iwrite(s, indent + 2, "'{}'".format(c.child_list[0]))
                else:
                    self.iwrite(
                        s, indent + 2, "{} = '{}'".format(c.name, c.child_list[0])
                    )
            else:
                c.get_str(s, indent + 2)
        self.iwrite(s, indent, "]".format())

    def iwrite(self, s, indent, line):
        s.write("{}{}\n".format(" " * indent, line))

    def get_sort_key(self):
        key_list = [self.name]
        for c in self.child_list:
            if isinstance(c, str):
                pass
            elif c.is_text_node:
                key_list.append([c.child_list[0]])
            else:
                key_list.append(c.get_sort_key())
        return key_list

    def sortme(self):
        for c in self.child_list:
            if isinstance(c, str):
                pass
            elif c.is_text_node:
                pass
            else:
                c.sortme()
        self.child_list.sort(key=lambda n: n.get_sort_key())


StableTree = StableNode
