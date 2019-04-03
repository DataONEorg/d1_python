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
import os
import tempfile

import pytest

import d1_common.iter.path

import d1_test.d1_test_case

TEST_TREE_PATH = {
    "dir11": {
        "file11": None,
        "file12": None,
        "dir111": {
            "file1111": None,
            "file1112": None,
            "file1113": None,
            "file1114": None,
        },
        "dir112": {"dir1121": None},
        "dir113": {
            "file1131": None,
            "dir1131": {
                "file11311": None,
                "file11312": None,
                "dir11311": {},
                "dir11312": {},
            },
            "dir1132": {
                "file11321": None,
                "file11322": None,
                "dir11321": {
                    "dir113211": {
                        "dir1132111": {
                            "file11321111": None,
                            "file11321112": None,
                            "dir11321111": {"dir113211111": None},
                        }
                    }
                },
            },
        },
    },
    "dir12": {
        "dir121": {
            "file1211": None,
            "file1212": None,
            "file1213": None,
            "file1214": None,
        },
        "dir122": {"file1221": None, "file1222": None},
    },
    "dir13": {},
    "dir15": {"file151": None, "dir151": {}},
}


@pytest.fixture(scope="function")
def tree_path(request):
    def r(dir_path, branch_dict):
        for k, v in branch_dict.items():
            p = os.path.join(dir_path, k)
            if v is None:
                with open(p, "w") as f:
                    f.write(k)
            else:
                os.mkdir(p)
                r(p, v)

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        r(tmp_dir_path, TEST_TREE_PATH)

        yield tmp_dir_path


@pytest.mark.parametrize("return_dir_paths", [True, False])
@pytest.mark.parametrize("recursive", [True, False])
class TestFileIterator(d1_test.d1_test_case.D1TestCase):
    # /dir11
    # /dir11/dir111
    # /dir11/dir111/file1111
    # /dir11/dir111/file1112
    # /dir11/dir111/file1113
    # /dir11/dir111/file1114
    # /dir11/dir112
    # /dir11/dir112/dir1121
    # /dir11/dir113
    # /dir11/dir113/dir1131
    # /dir11/dir113/dir1131/dir11311
    # /dir11/dir113/dir1131/dir11312
    # /dir11/dir113/dir1131/file11311
    # /dir11/dir113/dir1131/file11312
    # /dir11/dir113/dir1132
    # /dir11/dir113/dir1132/dir11321
    # /dir11/dir113/dir1132/dir11321/dir113211
    # /dir11/dir113/dir1132/dir11321/dir113211/dir1132111
    # /dir11/dir113/dir1132/dir11321/dir113211/dir1132111/dir11321111
    # /dir11/dir113/dir1132/dir11321/dir113211/dir1132111/dir11321111/dir113211111
    # /dir11/dir113/dir1132/dir11321/dir113211/dir1132111/file11321111
    # /dir11/dir113/dir1132/dir11321/dir113211/dir1132111/file11321112
    # /dir11/dir113/dir1132/file11321
    # /dir11/dir113/dir1132/file11322
    # /dir11/dir113/file1131
    # /dir11/file11
    # /dir11/file12
    # /dir12
    # /dir12/dir121
    # /dir12/dir121/file1211
    # /dir12/dir121/file1212
    # /dir12/dir121/file1213
    # /dir12/dir121/file1214
    # /dir12/dir122
    # /dir12/dir122/file1221
    # /dir12/dir122/file1222
    # /dir13
    # /dir15
    # /dir15/dir151
    # /dir15/file151

    def _check(self, test_path, postfix_str, *path_list, **param_dict):
        tmp_path_list = self._add_tmp(path_list, test_path)
        found_path_list = self._normalize(
            d1_common.iter.path.path_generator(tmp_path_list, **param_dict), test_path
        )
        postfix_str += "_incdirs" if param_dict["return_dir_paths"] else ""
        postfix_str += "_recursive" if param_dict["recursive"] else ""
        self.sample.assert_equals(found_path_list, postfix_str)

    def _add_tmp(self, path_list, test_path):
        """Add tmp root to paths."""
        return [os.path.join(test_path, p) for p in path_list]

    def _normalize(self, itr, test_path):
        """Trim the /tmp/*/ section and sort for reproducibility."""
        return sorted([v[len(test_path) :] for v in itr])

    def test_1000(self, tree_path, return_dir_paths, recursive):
        """file_iter(): Empty dir."""
        self._check(
            tree_path,
            "empty",
            "dir13",
            return_dir_paths=return_dir_paths,
            recursive=recursive,
        )

    def test_1010(self, tree_path, return_dir_paths, recursive):
        """file_iter(): Dir with dir and file."""
        self._check(
            tree_path,
            "dir_file",
            "dir15",
            return_dir_paths=return_dir_paths,
            recursive=recursive,
        )

    def test_1020(self, tree_path, return_dir_paths, recursive):
        """file_iter(): Root of deeply nested."""
        self._check(
            tree_path,
            "dir_root_nested",
            "dir11",
            return_dir_paths=return_dir_paths,
            recursive=recursive,
        )

    @pytest.mark.parametrize(
        "sample_postfix,exclude_glob_list",
        [
            ("exclude_files", ["*"]),
            ("exclude_dirs", ["*/"]),
            ("exclude_named_dir", ["dir1*/"]),
            ("exclude_named_file", ["*11*"]),
        ],
    )
    def test_1030(
        self, tree_path, return_dir_paths, recursive, sample_postfix, exclude_glob_list
    ):
        """file_iter(): Root of deeply nested."""
        self._check(
            tree_path,
            "dir_root_exclude_{}".format(sample_postfix),
            "dir11",
            return_dir_paths=return_dir_paths,
            recursive=recursive,
            exclude_glob_list=exclude_glob_list,
        )
