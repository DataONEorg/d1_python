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
"""Render a SubjectInfo PyXB object to UI or image file.

Based on the ETE Toolkit for analysis and visualization of trees.

ETE is a somewhat large dependency, so it is not installed by default with the
DataONE stack. To install, follow the instructions on the ETE site:
    http://etetoolkit.org.

"""
# See the module level docstring if ImportError is raised here
import ete3

# Rendering

# Global
BRANCH_VERTICAL_MARGIN = 20
EDGE_COLOR = "Gray"
EDGE_WIDTH = 2

# Type Node
TYPE_NODE_FONT_SIZE_FILE = 14
TYPE_NODE_FONT_SIZE_BROWSE = 8
TYPE_NODE_RADIUS = 40

# Subject Node
SUBJECT_NODE_FONT_SIZE = 10

TYPE_NODE_COLOR_DICT = {
    "Equiv": "LightBlue",
    "Group": "LightGreen",
    "Member": "LightPink",
    "Person": "Orange",
    "Root": "LightGray",
    "Symbolic": "Gold",
}


SUBJECT_NODE_TAG = "is_subject_node"
TYPE_NODE_TAG = "is_type_node"


class SubjectInfoRenderer:
    """Render a SubjectInfoTree to UI or image file.

    - Based on the ETE Toolkit for analysis and visualization of trees.

    """

    def __init__(self, subject_info_tree):
        self._tree = ete3.Tree(name="Root")
        self._tree.add_feature(TYPE_NODE_TAG, True)
        self._render_type = None
        self._gen_etetoolkit_tree(self._tree, subject_info_tree)

    def render_to_image_file(
        self, image_out_path, width_pixels=None, height_pixels=None, dpi=90
    ):
        """Render the SubjectInfo to an image file.

        Args:
            image_out_path : str
                Path to where image image will be written. Valid extensions are
                ``.svg,`` ``.pdf``, and ``.png``.

            width_pixels : int
                Width of image to write.

            height_pixels : int
                Height of image to write, in pixels.

            dpi:
                Dots Per Inch to declare in image file. This does not change the
                resolution of the image but may change the size of the image when
                rendered.

        Returns:
            None

        """
        self._render_type = "file"
        self._tree.render(
            file_name=image_out_path,
            w=width_pixels,
            h=height_pixels,
            dpi=dpi,
            units="px",
            tree_style=self._get_tree_style(),
        )

    def browse_in_qt5_ui(self):
        """Browse and edit the SubjectInfo in a simple Qt5 based UI."""
        self._render_type = "browse"
        self._tree.show(tree_style=self._get_tree_style())

    def render_to_ascii_art(self):
        """Render the SubjectInfo to a string containing an "ASCII art" tree.

        Returns:     str         String containing an "ASCII art" representation of the
        tree.

        """
        self._render_type = "ascii"
        return self._tree.get_ascii()

    # Private

    def _gen_etetoolkit_tree(self, node, subject_info_tree):
        """Copy SubjectInfoTree to a ETE Tree."""
        for si_node in subject_info_tree.child_list:
            if si_node.type_str == TYPE_NODE_TAG:
                child = self._add_type_node(node, si_node.label_str)
            elif si_node.type_str == SUBJECT_NODE_TAG:
                child = self._add_subject_node(node, si_node.label_str)
            else:
                raise AssertionError(
                    'Unknown node type. type_str="{}"'.format(si_node.type_str)
                )
            self._gen_etetoolkit_tree(child, si_node)

    def _add_type_node(self, node, label):
        """Add a node representing a SubjectInfo type."""
        child = node.add_child(name=label)
        child.add_feature(TYPE_NODE_TAG, True)
        return child

    def _add_subject_node(self, node, subj_str):
        """Add a node containing a subject string."""
        child = node.add_child(name=subj_str)
        child.add_feature(SUBJECT_NODE_TAG, True)
        return child

    def _get_node_path(self, node):
        """Return the path from the root to ``node`` as a list of node names."""
        path = []
        while node.up:
            path.append(node.name)
            node = node.up
        return list(reversed(path))

    def _get_tree_style(self):
        ts = ete3.TreeStyle()
        # Global styles
        ts.show_scale = False
        ts.show_leaf_name = False
        ts.branch_vertical_margin = BRANCH_VERTICAL_MARGIN
        # Dynamic styles
        ts.layout_fn = self._layout
        return ts

    def _layout(self, node):
        """ETE calls this function to style each node before rendering.

        - ETE terms:
        - A Style is a specification for how to render the node itself
        - A Face defines extra information that is rendered outside of the node
        - Face objects are used here to provide more control on how to draw the nodes.

        """

        def set_edge_style():
            """Set the style for edges and make the node invisible."""
            node_style = ete3.NodeStyle()
            node_style["vt_line_color"] = EDGE_COLOR
            node_style["hz_line_color"] = EDGE_COLOR
            node_style["vt_line_width"] = EDGE_WIDTH
            node_style["hz_line_width"] = EDGE_WIDTH
            node_style["size"] = 0
            node.set_style(node_style)

        def style_subject_node(color="Black"):
            """Specify the appearance of Subject nodes."""
            face = ete3.TextFace(node.name, fsize=SUBJECT_NODE_FONT_SIZE, fgcolor=color)
            set_face_margin(face)
            node.add_face(face, column=0, position="branch-right")

        def style_type_node(color="Black"):
            """Specify the appearance of Type nodes."""
            face = ete3.CircleFace(
                radius=TYPE_NODE_RADIUS,
                color=TYPE_NODE_COLOR_DICT.get(node.name, "White"),
                style="circle",
                label={
                    "text": node.name,
                    "color": color,
                    "fontsize": (
                        TYPE_NODE_FONT_SIZE_FILE
                        if self._render_type == "file"
                        else TYPE_NODE_FONT_SIZE_BROWSE
                    ),
                },
            )
            set_face_margin(face)
            node.add_face(face, column=0, position="branch-right")

        def set_face_margin(face):
            """Add margins to Face object.

            - Add space between inner_border and border on TextFace.
            - Add space outside bounding area of CircleFace.

            """
            face.margin_left = 5
            face.margin_right = 5
            # face.margin_top = 5
            # face.margin_bottom = 5

        set_edge_style()

        if hasattr(node, SUBJECT_NODE_TAG):
            style_subject_node()
        elif hasattr(node, TYPE_NODE_TAG):
            style_type_node()
        else:
            raise AssertionError("Unknown node type")
