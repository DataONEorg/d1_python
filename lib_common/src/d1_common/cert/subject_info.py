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
"""Utilities for handling the DataONE SubjectInfo type.

Overview of Access Control in DataONE
-------------------------------------

Access control in DataONE works much like traditional Access Control Lists (ACLs). Each
science object is associated with an ACL. The ACL contains a list of subjects and an
access level for each subject. The access levels are `read`, `write` and
`changePermission`. Each access level implicitly grants access to the lower levels, so
only only the highest access level for a given subject needs to be specified in the ACL.

This module handles the information that will be used for creating a list of
authenticated subjects that can be compared against an ACL in order to determine if a
given subject is allowed to access the object at the requested level.

DataONE supports a system where subjects can be linked to equivalent identities as well
as managed in groups. E.g., a group of subjects can be created and all the subjects in
the group can be given access to an object by only listing the single group subject in
the object's ACL.

A given subject can describe an actual identity, an equivalent subject or a group
subject. Any type of subject can be used in any capacity. E.g., each subject in a group
can be any type of subject including another group.

Since ACLs can also contain any combination of subjects for actual identities,
equivalent subjects and groups subjects, a list of subjects that includes all subjects
that are associated with an authenticated subject is required in order to determine if
access should be granted.

Arbitrarily nested subjects must be supported. E.g., If subj-1 has been successfully
authenticated, and subj-1 has an equivalent subject called equiv-1, and equiv-1 is in a
group with subject group-1, all of those subjects (subj-1, equiv-1, and group-1), must
be included in the list of associated subjects. That way, access is granted to the
object regardless of which of them are authenticated directly in the ACL.

Notes
-----

- It's important to separate the roles of groups in the ACL and groups in the
  SubjectInfo. Including a group subject in an ACL grants access to all subjects in
  that group. However, including a subject that is in a group, in the ACL, does not
  give access to the other subjects of the group or to the group itself. In other
  words, groups add access for their members, not the other way around.

- In terms of generating a list of equivalent subjects based on SubjectInfo, the one
  way transfer of access from groups to their subjects means that, when a subject is
  found to belong to a group, only the group subject is included in the list (after
  which it may chain to more equivalent identifies, etc). The group members are not
  included.

- For deriving a list of indirectly authenticated subjects, the SubjectInfo contains a
  set of statements that establish subject types and relationships between subjects.
  There are 4 kinds of statements:

  - Subject is a person
  - Subject is an equivalent of another subject
  - Subject is a group
  - Subject is member of a group

- An equivalent subject can only be the equivalent for a person. The equivalence
  relationship is the only one that causes each side to be granted all the rights of
  the other side, and so allows the two subjects to be used interchangeably. The other
  relationships cause one side to be granted the rights of the other side, but not the
  other way around. E.g.: Designating a subject as a member of a group causes the
  subject to be granted the rights of the group, but does not cause the group to be
  granted the rights of the subject.


Authorization examples
----------------------

Given SubjectInfo::

    A = person subject A, authenticated by certificate
    B = person subject B

    C = equivalent to A
    D = equivalent to B
    E = equivalent to D

    F = group with members G, H, B
    J = group with members K, L, F
    M = group with members E, N
    N = group with members C, D


Given ACL containing: D
~~~~~~~~~~~~~~~~~~~~~~~

- D is equivalent to B
- B is a Person, but it's unauthenticated

Authorization: Denied


Given ACL containing: N
~~~~~~~~~~~~~~~~~~~~~~~

- N is a group with members C and D
- D is equivalent to B, but B is not authenticated
- C is equivalent to A, and A is authenticated

Authorization: Granted


Given ACL containing: F
~~~~~~~~~~~~~~~~~~~~~~~

- F leads to G, H, B
- G -> unknown
- H -> unknown
- B -> person subject, but not authenticated

Authorization: Denied

"""
import os

import d1_common.const
import d1_common.types.exceptions
import d1_common.xml

SUBJECT_NODE_TAG = "is_subject_node"
TYPE_NODE_TAG = "is_type_node"


def extract_subjects(subject_info_xml, primary_str):
    """Extract a set of authenticated subjects from a DataONE SubjectInfo.

    - See subject_info_tree for details.

    Args:
        subject_info_xml : str
            A SubjectInfo XML document.

        primary_str : str
            A DataONE subject, typically a DataONE compliant serialization of the DN of
            the DataONE X.509 v3 certificate extension from which the SubjectInfo was
            extracted.

            The primary subject can be viewed as the root of a tree. Any subject in the
            SubjectInfo that is directly or indirectly connected to the root subject is
            included in the returned set of authenticated subjects.


    Returns:
        set: Set of authenticated subjects. Will always include the primary subject.

        - All subjects in the returned set are equivalent to ``primary_str`` for the
          purpose of access control for private science objects.

        - If SubjectInfo does not contain all relevant records, it is still considered
          to be valid, but the authenticated set will be incomplete.

        - Only the subject strings and relationships in SubjectInfo are used by this
          function. Other information about subjects, such as name and email address,
          is ignored.

        - No attempt should be made to infer type of subject from the content of a
          subject string. Subject strings should be handled as random Unicode
          sequences, each of which may designate an person subject, an equivalent
          subject, or a group subject.

        - To determine if an action is authorized, the returned set is checked against
          the authorized_set for a given object. If one or more subjects exist in both
          sets, the action is authorized. The check can be performed with high
          performance using a set union operation in Python or an inner join in
          Postgres.

        - Subject types are only known and relevant while processing the SubjectInfo
          type.
        - The type of each subject in the authenticated_subjects and allowed_subjects
          lists are unknown and irrelevant.

    Notes:
        Procedure:

        The set of authenticated subjects is generated from the SubjectInfo and primary
        subject using the following procedure:

        - Start with empty set of subjects
        - Add authenticatedUser
        - If ``subject`` is not in set of subjects:
        - Add ``subject``
        - Iterate over Person records
        - If Person.subject is ``subject``:
        - If Person.verified is present and set:
        - Add "verifiedUser"
        - Iterate over Person.equivalentIdentity:
        - Recursively add those subjects
        - Iterate over Person.isMemberOf
        - Recursively add those subjects, but ONLY check Group subjects
        - Iterate over Group records
        - If any Group.hasMember is ``subject``:
        - Recursively add Group.subject (not group members)


        Handling of various invalid SubjectInfo and corner cases:

        - SubjectInfo XML doc that is not well formed
        - Return an exception that includes a useful error message with the line number
          of the issue

        - person.isMemberOf and group.hasMember should always form pairs referencing
          each other.
        - One side of the pair is missing
        - Process the available side as normal
        - person.isMemberOf subject references a person or equivalent instead of a
          group
        - Only Group subjects are searched for isMemberOf references, so only the
          referenced Group subject is added to the list of authorized subjects

        - Multiple Person or Group records conflict by using the same subject
        - The records are handled as equivalents

        - person.isMemberOf subject does not reference a known subject
        - If the Person containing the dangling isMemberOf IS NOT connected with the
          authenticated subject, the whole record, including the isMemberOf subject is
          simply ignored
        - If it IS connected with an authenticated subject, the isMemberOf subject is
          authenticated and recursive processing of the subject is skipped

        - Circular references
        - Handled by skipping recursive add for subjects that are already added

        - See the unit tests for example SubjectInfo XML documents for each of these
          issues and the expected results.

    """
    subject_info_pyxb = deserialize_subject_info(subject_info_xml)
    subject_info_tree = gen_subject_info_tree(subject_info_pyxb, primary_str)
    return subject_info_tree.get_subject_set()


def deserialize_subject_info(subject_info_xml):
    """Deserialize SubjectInfo XML doc to native object.

    Args:
        subject_info_xml: str
            SubjectInfo XML doc

    Returns:
        SubjectInfo PyXB object

    """
    try:
        return d1_common.xml.deserialize(subject_info_xml)
    except ValueError as e:
        raise d1_common.types.exceptions.InvalidToken(
            0,
            'Could not deserialize SubjectInfo. subject_info="{}", error="{}"'.format(
                subject_info_xml, str(e)
            ),
        )


# noinspection PyTypeChecker
def gen_subject_info_tree(subject_info_pyxb, authn_subj, include_duplicates=False):
    """Convert the flat, self referential lists in the SubjectInfo to a tree structure.

    Args:
        subject_info_pyxb: SubjectInfo PyXB object

        authn_subj: str
            The authenticated subject that becomes the root subject in the tree of
            subjects built from the SubjectInfo.

            Only subjects that are authenticated by a direct or indirect connection to
            this subject are included in the tree.

        include_duplicates:
            Include branches of the tree that contain subjects that have already been
            included via other branches.

            If the tree is intended for rendering, including the duplicates will
            provide a more complete view of the SubjectInfo.

    Returns:
        SubjectInfoNode : Tree of nodes holding information about subjects that are
        directly or indirectly connected to the authenticated subject in the root.

    """

    class State:
        """self."""

        pass

    state = State()

    state.subject_info_pyxb = subject_info_pyxb
    state.include_duplicates = include_duplicates
    state.visited_set = set()
    state.tree = SubjectInfoNode("Root", TYPE_NODE_TAG)

    _add_subject(state, state.tree, authn_subj)
    symbolic_node = state.tree.add_child("Symbolic", TYPE_NODE_TAG)
    _add_subject(state, symbolic_node, d1_common.const.SUBJECT_AUTHENTICATED)
    _trim_tree(state)

    return state.tree


def _add_subject(state, node, subject_str, group_only=False):
    if state.include_duplicates:
        subj_node = node.add_child(subject_str, SUBJECT_NODE_TAG)
    if subject_str in state.visited_set:
        return
    if not state.include_duplicates:
        subj_node = node.add_child(subject_str, SUBJECT_NODE_TAG)
    state.visited_set.add(subject_str)
    if not group_only:
        # noinspection PyUnboundLocalVariable
        _add_person(state, subj_node, subject_str)
    _add_group_elements(state, subj_node, subject_str)


def _add_person(state, node, subject_str):
    for person_pyxb in state.subject_info_pyxb.person:
        if person_pyxb.subject.value() == subject_str:
            person_node = node.add_child("Person", TYPE_NODE_TAG)
            _add_person_subject(state, person_node, person_pyxb)
            _add_person_equivalent_subjects(state, person_node, person_pyxb)
            _add_person_is_member_of(state, person_node, person_pyxb)
    return node


def _add_person_subject(state, node, person_pyxb):
    _add_subject(state, node, person_pyxb.subject.value())
    if person_pyxb.verified:
        symbolic_node = node.add_child("Symbolic", TYPE_NODE_TAG)
        _add_subject(state, symbolic_node, d1_common.const.SUBJECT_VERIFIED)


def _add_person_is_member_of(state, node, person_pyxb):
    member_of_node = node.add_child("Member", TYPE_NODE_TAG)
    for is_member_of_pyxb in person_pyxb.isMemberOf:
        _add_subject(state, member_of_node, is_member_of_pyxb.value(), group_only=True)


def _add_person_equivalent_subjects(state, node, person_pyxb):
    equivalent_node = node.add_child("Equiv", TYPE_NODE_TAG)
    for equivalent_pyxb in person_pyxb.equivalentIdentity:
        _add_subject(state, equivalent_node, equivalent_pyxb.value())


def _add_group_elements(state, node, subject_str):
    group_node = node.add_child("Group", TYPE_NODE_TAG)
    for group_pyxb in state.subject_info_pyxb.group:
        if _subject_is_member_of_group(group_pyxb, subject_str):
            _add_subject(state, group_node, group_pyxb.subject.value())


def _subject_is_member_of_group(group_pyxb, subject_str):
    for member_pyxb in group_pyxb.hasMember:
        if member_pyxb.value() == subject_str:
            return True
    return False


def _trim_tree(state):
    """Trim empty leaf nodes from the tree.

    - To simplify the tree conversion, empty nodes are added before it is known if they
      will contain items that connect back to the authenticated subject. If there are
      no connections, the nodes remain empty, which causes them to be removed here.

    - Removing a leaf node may cause the parent to become a new empty leaf node, so the
      function is repeated until there are no more empty leaf nodes.

    """
    for n in list(state.tree.leaf_node_gen):
        if n.type_str == TYPE_NODE_TAG:
            n.parent.child_list.remove(n)
            return _trim_tree(state)


class SubjectInfoNode:
    """Tree representation of SubjectInfo.

    In SubjectInfo, nested information is represented via self- referential lists. This
    class holds a recursive tree of nodes which simplifies processing of SubjectInfo for
    client apps.

    """

    SUBJECT_NODE_TAG = "is_subject_node"
    TYPE_NODE_TAG = "is_type_node"

    def __init__(self, label_str, type_str):
        self.parent = None
        self.child_list = []
        self.type_str = type_str
        self.label_str = label_str

    def add_child(self, label_str, type_str):
        """Add a child node."""
        child_node = SubjectInfoNode(label_str, type_str)
        child_node.parent = self
        self.child_list.append(child_node)
        return child_node

    @property
    def node_gen(self):
        """Generate all nodes for the tree rooted at this node.

        Yields:     SubjectInfoNode         All nodes rooted at this node.

        """
        for n in self.child_list:
            yield from n.node_gen
        yield self

    @property
    def leaf_node_gen(self):
        """Generate all leaf nodes for the tree rooted at this node.

        Yields:     SubjectInfoNode         All leaf nodes rooted at this node.

        """
        return (v for v in self.node_gen if v.is_leaf)

    @property
    def parent_gen(self):
        """Generate this node, then all parents from this node to the root.

        Yields:     SubjectInfoNode         This node, then all parents from this node
        to the root.

        """
        yield self
        if self.parent is not None:
            yield from self.parent.parent_gen

    def get_path_str(self, sep=os.path.sep, type_str=None):
        """Get path from root to this node.

        Args:
            sep: str
                One or more characters to insert between each element in the path.
                Defaults to "/" on Unix and "\" on Windows.

            type_str:
                SUBJECT_NODE_TAG, TYPE_NODE_TAG or None. If set, only include
                information from nodes of that type.

        Returns:
            str: String describing the path from the root to this node.

        """
        return sep.join(
            list(
                reversed(
                    [
                        v.label_str
                        for v in self.parent_gen
                        if type_str in (None, v.type_str)
                    ]
                )
            )
        )

    def get_leaf_node_path_list(self, sep=os.path.sep, type_str=None):
        """Get paths for all leaf nodes for the tree rooted at this node.

        Args:
            sep: str
                One or more characters to insert between each element in the path.
                Defaults to "/" on Unix and "\" on Windows.

            type_str:
                SUBJECT_NODE_TAG, TYPE_NODE_TAG or None. If set, only include
                information from nodes of that type.

        Returns:
            list of str: The paths to the leaf nodes for the tree rooted at this node.

        """
        return [v.get_path_str(sep, type_str) for v in self.leaf_node_gen]

    def get_path_list(self, type_str=None):
        """Get list of the labels of the nodes leading up to this node from the root.

        Args:
            type_str:
                SUBJECT_NODE_TAG, TYPE_NODE_TAG or None. If set, only include
                information from nodes of that type.

        Returns:
            list of str: The labels of the nodes leading up to this node from the root.

        """
        return list(
            reversed(
                [v.label_str for v in self.parent_gen if type_str in (None, v.type_str)]
            )
        )

    @property
    def is_leaf(self):
        """Return True if this is a leaf node (has no children)"""
        return len(self.child_list) == 0

    def get_label_set(self, type_str=None):
        """Get a set of label_str for the tree rooted at this node.

        Args:
            type_str:
                SUBJECT_NODE_TAG, TYPE_NODE_TAG or None. If set, only include
                information from nodes of that type.

        Returns:
            set: The labels of the nodes leading up to this node from the root.

        """
        return {v.label_str for v in self.node_gen if type_str in (None, v.type_str)}

    def get_subject_set(self):
        """Get a set of subjects for the tree rooted at this node.

        Returns:     set: The subjects for the tree rooted at this node.

        """
        return self.get_label_set(SUBJECT_NODE_TAG)


# Every node is the root of a subtree. The root node is the root of the whole tree.
SubjectInfoTree = SubjectInfoNode
