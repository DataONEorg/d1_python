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

"""Generate a str that contains a normalized representation of an XML document.

For unit testing, we want to be able to store and compare samples representing XML
documents that are guaranteed to be stable.

Often, XML docs have various sections containing unordered sets of elements where there
are no semantics associated with the order in which they appear in the doc. The same is
true for element attributes. For DataONE, typical examples are lists of subjects,
permission rules and services.

Since the source for such elements are often dict and set based containers that
themselves don't provide deterministic ordering, serializing a group of such objects
can generate a large number of possible XML docs that, while semantically identical,
cannot be directly compared as text or in the DOM.

Normalizing the formatting can be done with a single deserialize to DOM and back to
XML, but that will not normalize the ordering of the elements, Without a schema,
automated tools cannot rearrange elements in an XML doc, since it is not known if the
order is significant. However, for generating and comparing XML doc samples, a stable
document that contains all the information from the XML doc is sufficient.

The strategy for generating a stable representation of an XML doc is as follows:

- All sibling XML elements must be sorted regardless of where they are in the tree.

- Each element is the root of a branch of the node tree. Sorting, of course, is based
  on comparing individual elements in order to determine their relative orderings. If
  the information in the elements themselves is identical, it is necessary to break the
  tie by recursively comparing their descendants until either a difference is found, or
  the two elements are determined to be the roots of two identical branches.

- To enable the sort algorithm to compare the branches, sort keys that hold all
  information in the branch are generated and passed to the sort. For comparisons to
  properly compare elements in the most to least significant order, each node in the
  branch must be in a single list item. So the key is a nested list of lists.

- Finally, since the sort keys are generated from the descendants, siblings in a given
  element can only be sorted after all their descendants in the tree have been sorted.
  So the tree must be traversed depth first, and the sort performed as the algorithm is
  stepping up from a completed level.

- To avoid having to build a new tree depth first, inline sort is used.

Notes:

    # RDF-XML

    Although the hierarchical structure of elements is almost always significant in XML,
    there are instances where semantically identical XML docs can have different
    hierarchies. This often occurs when generating RDF-XML docs from RDF.

    This module only normalizes the ordering of sibling elements and attributes.
    Parent-child relationships are never changed. So RDF-XML docs generated in such a way
    that parent-child relationships may differ without change in semantics are not
    supported.

    ## Background

    RDF is an unordered set of subject-predicate-object triples. Triples cannot share
    values, so when there are multiple triples for a subject, each triple must contain a
    copy of the subject.

    RDF-XML supports expressing triples with less redundancy by factoring shared values out
    to parent elements. E.g., a set of triples for a subject can be expressed as a series
    of predicate-object children with a single subject parent.

    When generating RDF-XML from RDF that contains many triples that share values, the same
    set of triples can be represented by many different hierarchies. The hierarchy that is
    actually generated depends on the algorithm and may also depend on the order in which
    the triples are processed. If the triples are retrieved from an unordered set, the
    processing order is pseudo-random, causing pseudo-random variations in the generated
    hierarchy.

"""


import io

import d1_common.type_conversions


def get_normalized_xml_representation(xml):
    """Return a str that contains a normalized representation of an XML document."""

    return str(xml_to_stabletree(xml))


def xml_to_stabletree(xml):
    """Return a StableTree that contains a normalized representation of an XML
    document."""

    etree = d1_common.type_conversions.str_to_etree(xml)
    stable_tree = etree_to_stable_tree(etree)
    stable_tree.sort()
    return stable_tree


def etree_to_stable_tree(et_node):
    """Convert an ElementTree to a StableTree.

    - Node attributes become @key:string - Text elements become @text:string - name is
      the name of the xml element

    """

    # element name
    et_tag = d1_common.type_conversions.replace_namespace_with_prefix(et_node.tag)
    stable_node = StableNode(et_tag)
    # element attributes
    for k, v in getattr(et_node, "attrib", {}).items():
        stable_node.add_child(
            StableNode(
                "@" + d1_common.type_conversions.replace_namespace_with_prefix(k),
                StableNode(v),
            )
        )
    # element text node
    if et_node.text and et_node.text.strip() != "":
        stable_node.add_child(StableNode("#text", StableNode(et_node.text.strip())))
    # et_child elements
    for et_child in list(et_node):
        stable_node.add_child(etree_to_stable_tree(et_child))
    return stable_node


class StableNode:
    """Tree structure that uses lists instead of dicts, as lists have deterministic
    ordering."""

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

    def add_child(self, e):
        self.child_list.append(e)

    def get_str(self, s, indent):
        def indent_write(indent_, line):
            s.write("{}{}\n".format(" " * indent_, line))

        indent_write(indent, "{} = [".format(self.name))

        for c in self.child_list:
            if isinstance(c, StableNode):
                c.get_str(s, indent + 2)
            else:
                indent_write(indent + 2, "'{}'".format(c))

        indent_write(indent, "]".format())

    def get_sort_key_(self):
        return [self.name] + [
            (c.get_sort_key_() if isinstance(c, StableNode) else c)
            for c in self.child_list
        ]

    def sort(self, p=None):
        p = p or []
        for c in self.child_list:
            if isinstance(c, StableNode):
                c.sort(p + [c.name])
        self.child_list.sort(key=lambda n: n.get_sort_key_())


StableTree = StableNode
