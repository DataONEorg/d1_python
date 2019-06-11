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


import logging
import d1_gmn.tests.gmn_test_case

# Database key matching a key in settings_test.DATABASE
TEMPLATE_DB_KEY = "default"

# Path to fixture created with ``mk_db_fixture``.
REL_DB_FIXTURE_PATH = "json/db_fixture.json.bz2"


def main():
    logger = logging.getLogger(__name__)
    logger.info("Creating GMN test template DB...")

    db_name = d1_gmn.tests.gmn_test_case.django_get_db_name_by_key(TEMPLATE_DB_KEY)
    d1_gmn.tests.gmn_test_case.postgres_drop_if_exists(db_name)
    d1_gmn.tests.gmn_test_case.postgres_create_blank(db_name)
    d1_gmn.tests.gmn_test_case.django_migrate(TEMPLATE_DB_KEY)
    d1_gmn.tests.gmn_test_case.django_populate_by_json(TEMPLATE_DB_KEY, REL_DB_FIXTURE_PATH)

    d1_gmn.tests.gmn_test_case.django_dump_db_stats()


if __name__ == "__main__":
    main()
