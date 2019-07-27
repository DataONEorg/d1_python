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

"""Find the software stack and version for each MN in a DataONE environment.

The results are printed to stdout and written to a CSV file.

The MNs are checked concurrently, while checks are issued to each MN serially. This
gives each MN the most time to return something sensible but does end up slowing down
the script, since it ends up waiting until timeout for each check against dead nodes.
"""

import asyncio
import csv
import logging
import re
import ssl
import sys

import aiohttp
import bs4

import d1_scimeta.util

import d1_common.env
import d1_common.url
import d1_common.util
import d1_common.utils.ulog
import d1_common.wrap.simple_xml

import d1_client.cnclient_2_0
import d1_client.command_line

TIMEOUT_SECONDS = 30
RESULT_CSV_PATH = "./node_versions.csv"
# Max number of lines to log from unrecognized response body
MAX_RESPONSE_LINE_COUNT = 10

log = logging.getLogger(__name__)


def main():
    """Sync wrapper of main() for use by d1_util.setup() to generate console entry
    points."""
    sys.exit(asyncio.run(_main()))


async def _main():
    parser = d1_client.command_line.D1ClientArgParser(__doc__)
    parser.add_argument(
        "csv_path",
        nargs="?",
        default=RESULT_CSV_PATH,
        help="Save path for version information CSV file",
    )
    parser.add_argument(
        "--max_response_lines",
        "-m",
        type=int,
        default=MAX_RESPONSE_LINE_COUNT,
        help="Max number of lines to log from unrecognized response body",
    )
    parser.add_argument(
        "--only",
        "-n",
        nargs="*",
        default=[],
        metavar="regex",
        help="Only check nodes with baseURL matching regex",
    )

    args = parser.parse_args()
    d1_client.command_line.log_setup(args.debug)
    args_dict = parser.get_method_args(args)
    cn_base_url = args_dict["base_url"]
    node_list_pyxb = get_node_list_pyxb(cn_base_url)

    base_url_list = get_eligible_base_url_list(node_list_pyxb)

    if args.only:
        base_url_list = filter_by_rx_list(args.only, base_url_list)

    log.info("Node count: {}".format(len(base_url_list)))

    if not base_url_list:
        return 1

    log.info("Creating one type/version task per node")
    task_set = set()
    result_list = []
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=TIMEOUT_SECONDS)
    ) as session:
        for base_url in base_url_list:
            log.info(f'Adding node. base_url="{base_url}"')
            task_set.add(get_node_type_and_version(session, base_url))

        log.info("Processing tasks")
        while True:
            done_set, task_set = await asyncio.wait(
                task_set, return_when=asyncio.FIRST_COMPLETED
            )
            log.info("Task completed. Remaining tasks: {}".format(len(task_set)))
            for task in done_set:
                result_list.append(task.result())
            if not task_set:
                break

    log.info("Saving results")
    tidy_list = get_tidy_list(result_list)
    print_result(tidy_list)
    write_result_csv(RESULT_CSV_PATH, tidy_list)
    log.info("Wrote result to: {}".format(RESULT_CSV_PATH))


async def get_node_type_and_version(session, base_url):
    """Try software stack type and version extraction algorithms on MN until one is
    successful or all have been tried.

    If none are successful, return the status code and response body from the last
    failed attempt.

    Args:
        session: aiohttp.ClientSession
        base_url: Member Node BaseURL

    Returns:
        If successful:
            baseURL of recognized MN: str
            type of MN: str ("GMN" or "Metacat")
            software stack version: str
    """
    gmn_version_str = await get_gmn_version(session, base_url)
    if gmn_version_str:
        return base_url, "GMN", gmn_version_str
    if await is_v1_gmn(session, base_url):
        return base_url, "GMN", "1.x.x"
    metacat_version_str = await get_metacat_version(session, base_url)
    if metacat_version_str:
        return base_url, "Metacat", metacat_version_str
    base_url, status_int, result_str = await check_api_endpoints(session, base_url)
    log.debug("Received result: {}".format(base_url))
    return base_url, status_int, result_str


async def get_gmn_version(session, base_url):
    """Get version number returned from /home by GMN 1.x / 2.x / 3.x.

    Args:
        session:
        base_url (): The BaseURL of a node that may be a GMN instance.

    Returns:
        None: The node at base_url is not a functional GMN instance
        str: The node at base_url is a functional GMN instance running the returned version.
    """
    home_url = d1_common.url.joinPathElements(base_url, "home")
    log.info("Checking for GMN: {}".format(base_url))
    status, body_str = await get(session, home_url)
    if status in (200, 401):
        version_str = await get_gmn_1x_2x_version(body_str)
        if version_str:
            return version_str

        version_str = await get_gmn_3x_version(body_str)
        if version_str:
            return version_str

        dump_response_body("/home exists but returned unrecognized response", body_str)


async def get_gmn_1x_2x_version(html_str):
    """Get version number from HTML returned from /home by GMN 1.x / 2.x.

    GMN 1.x / 2.x /home endpoint returns HTML which must be scraped for the version
    number.

    Args:
        html_str: HTTP body that may be HTML returned from a GMN 1.x / 2.x instance.

    Returns:
        None: ``html_str`` is not valid HTML from a GMN 1.x / 2.x instance.
        str: ``html_str`` is from a GMN 1.x / GMN 2.x instance running the returned
        version.
    """
    try:
        soup = bs4.BeautifulSoup(html_str, "html.parser")
        return soup.find(string="GMN version:").find_next("td").string
    except AttributeError:
        pass


async def get_gmn_3x_version(xml_str):
    """Get version number from XML returned from /home by GMN 3.x.

    GMN 3.x /home endpoint returns well formed XML containing version numbers for
    components in the stack.

    Returns:
        None: ``xml_str`` is not valid XML from a GMN 3.x instance.
        str: ``xml_str`` is from a GMN 3.x instance running the returned version

    XML fragment:
        <value name="gmnVersion">3.4.2</value>
    """
    try:
        with d1_common.wrap.simple_xml.wrap(xml_str) as xml:
            return xml.get_element_by_xpath('//value[@name="gmnVersion"]')[0].text
    except (d1_common.wrap.simple_xml.SimpleXMLWrapperException, IndexError):
        pass


async def is_v1_gmn(session, base_url):
    """Detect GMN v1 where version cannot be determined due to access restricted
    ObjectList, 500 ServiceFailure or other issues.

    Args:
        session:
        base_url: str
            The BaseURL of a node that may be a GMN v1 instance.

    Returns:

    """
    status, body_str = await get(session, base_url)
    return '<h3><font style="color:red">' in (body_str or "")


async def get_metacat_version(session, base_url):
    """
    Args:
        session:
        base_url: The BaseURL of a node that may be a Metacat instance.

    Returns:
        None: The node at base_url is not a functional Metacat instance.
        str: The node at base_url is a functional Metacat instance running the returned version.
    """
    log.info("Checking for Metacat: {}".format(base_url))
    metacat_version_url = base_url.strip("/d1/mn") + "/metacat?action=getversion"
    status, body_str = await get(session, metacat_version_url)
    if status == 200:
        xml_tree = d1_scimeta.util.parse_xml_bytes(body_str.encode("utf-8"))
        # d1_scimeta.util.dump_pretty_tree(xml_tree)
        return xml_tree.getroot().text


async def check_api_endpoints(session, base_url):
    """Check for recognizable response from: v1/node, v2/node, v2/object, v1/object,
    baseURL.

    To maximize the chance of receiving a response, the endpoints are checked serially
    instead of concurrently.

    Endpoints are checked in the order listed. If valid response is received,
    information about the successful request is returned and later endpoints are not
    checked.

    If no checks are successful, result from the last unsuccessful check is returned.

    Note: The run time of the entire script will be pretty much equal to the timeout times
    This function takes up the most time. It typically waits until timeout for
    each of the checked endpoints.
    """
    status_int = "?"
    for check_str in "v1/node", "v2/node", "v2/object", "v1/object", "/":
        api_url = d1_common.url.joinPathElements(base_url, check_str)
        log.info("Checking unknown: {}".format(api_url))
        status, body_str = await get(session, api_url)
        if status in (200, 401):
            break
    return base_url, status_int, f"{check_str}={body_str}"


async def get(session, url):
    """Wrapper for session.get() that returns None if the HTTP GET call failed.

    Args:
        session:
        url:

    Returns:
        2-tup
            status_code: int
            body_str: str
    """
    try:
        async with session.get(url, ssl=False) as response:
            return response.status, await response.text()
    except (
        ssl.SSLError,
        asyncio.TimeoutError,
        ConnectionError,
        aiohttp.ClientConnectorError,
    ):
        return None, None


def filter_by_rx_list(rx_list, base_url_list):
    filtered_base_url_set = set()
    for rx in rx_list:
        for base_url in base_url_list:
            if re.search(rx, base_url):
                if base_url not in filtered_base_url_set:
                    log.debug(f"Including node selected by regex: {rx}: {base_url}")
                filtered_base_url_set.add(base_url)
    return sorted(filtered_base_url_set)


def get_tidy_list(response_list):
    def trim(v):
        return " / ".join(str(v).splitlines())[:80]

    return [
        (trim(v[1]), trim(v[2]), trim(v[0]))
        for v in sorted(response_list, key=lambda x: (str(x[1]), x[2], x[0]))
    ]


def print_result(tidy_list):
    for row_list in tidy_list:
        log.info("{:<10} {:<10} {}".format(row_list[0], row_list[1], row_list[2]))


def write_result_csv(result_csv_path, tidy_list):
    with open(result_csv_path, "w") as csv_file:
        csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(
            [
                "node_type or status code",
                "version or first line of unrecognized html body",
                "base_url",
            ]
        )
        for row_list in tidy_list:
            csv_writer.writerow(row_list)


def get_node_list_pyxb(cn_base_url):
    client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(cn_base_url)
    return client.listNodes()


def get_eligible_base_url_list(node_list_pyxb):
    eligible_base_url_list = []
    for node_pyxb in node_list_pyxb.node:
        if node_pyxb.type == "cn":
            log.debug("Skipping CN: {}".format(node_pyxb.baseURL))
        elif node_pyxb.state != "up":
            log.debug(
                f'Skipping node with state "{node_pyxb.state}": {node_pyxb.baseURL}'
            )
        else:
            eligible_base_url_list.append(node_pyxb.baseURL)
    return eligible_base_url_list


def dump_response_body(msg_str, body_str):
    log.warning(f"{msg_str}:")
    for i, line in enumerate(body_str.splitlines(keepends=False)):
        if i == MAX_RESPONSE_LINE_COUNT:
            log.warning("  <skipped rest of response body>")
            break
        log.warning("  {:>4} {}".format(i + 1, line))


if __name__ == "__main__":
    sys.exit(main())
