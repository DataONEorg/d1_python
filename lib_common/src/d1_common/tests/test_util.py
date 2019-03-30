#!/usr/bin/env python

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
import copy

import pytest

import d1_common.util

import d1_test.d1_test_case


@pytest.fixture(
    scope="function",
    params=[
        {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "verbose": {
                    "format": "%(asctime)s %(levelname)-8s %(name)s %(module)s "
                    "%(process)d %(thread)d %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "rotating_file": {
                    "level": "DEBUG",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": "/tmp/test/log/file/path",
                    "maxBytes": 10 * 1024 * 1024,
                    "backupCount": 5,
                    "formatter": "verbose",
                },
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "verbose",
                    "level": "DEBUG",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                "": {"handlers": ["rotating_file"], "level": "DEBUG", "propagate": True}
            },
        }
    ],
)
def dict_config_fixture(request):
    yield copy.deepcopy(request.param)


class TestCommonUtil(d1_test.d1_test_case.D1TestCase):
    def test_1010(self, dict_config_fixture):
        """nested_update(): Update existing values."""
        # dict_config_fixture = copy.deepcopy(TEST_DICT)

        d1_common.util.nested_update(
            dict_config_fixture,
            {
                # Update existing values
                "handlers": {"rotating_file": {"maxBytes": 1234}},
                "loggers": {"": {"level": "new_level", "propagate": False}},
            },
        )
        # self.sample.gui_sxs_diff(TEST_DICT, dict_config_fixture)
        self.sample.assert_equals(dict_config_fixture, "nested_update_existing")

    def test_1020(self, dict_config_fixture):
        """nested_update(): Add new keys in existing tree."""
        d1_common.util.nested_update(
            dict_config_fixture,
            {
                #
                "handlers": {
                    "new_key_1": {
                        "level": "new_level",
                        "l1": {
                            "l2": {
                                "key3": "val1",
                                "l3": {
                                    "key3": "val2",
                                    "l4": {"l5": {"key1": "val3", "key2": "val4"}},
                                },
                            }
                        },
                    }
                }
            },
        )
        # self.sample.gui_sxs_diff(TEST_DICT, dict_config_fixture)
        self.sample.assert_equals(dict_config_fixture, "nested_update_new")

    def test_1030(self, dict_config_fixture):
        """nested_update(): Combined."""
        d1_common.util.nested_update(
            dict_config_fixture,
            {
                # Update existing values
                "handlers": {"rotating_file": {"maxBytes": 1234}},
                "loggers": {
                    "": {"level": "new_level", "propagate": False},
                    # Add new keys in existing tree
                    "handlers": {
                        "new_key_1": {
                            "level": "new_level",
                            "l1": {
                                "l2": {
                                    "key3": "val1",
                                    "l3": {
                                        "key3": "val2",
                                        "l4": {"l5": {"key1": "val3", "key2": "val4"}},
                                    },
                                }
                            },
                        }
                    },
                    "formatters": {"verbose": {"format": "new_format"}},
                    "loggers": {"django": {"level": "new_level"}},
                },
                # Add new trees
                "l1": {
                    "l2": {
                        "key3": "val1",
                        "l3": {
                            "key3": "val2",
                            "l4": {"l5": {"key1": "val3", "key2": "val4"}},
                        },
                    }
                },
                "key3": "val5",
                "lb1": {
                    "key5": "val6",
                    "l2": {"l3": {"l4": {"l5": {}}}, "key3": "val7"},
                    "key6": "val8",
                },
            },
        )
        # self.sample.gui_sxs_diff(TEST_DICT, dict_config_fixture)
        self.sample.assert_equals(dict_config_fixture, "nested_update_combined")
