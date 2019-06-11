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
"""Bulk download System Metadata object from MN.

This is an example on how to use the DataONE Client and Common libraries for Python. It
shows how to:

- Use the multiprocessed System Metadata iterator to efficiently perform bulk downloads
  of System Metadata from a Member Node

"""

import argparse
import logging
import os
import sys
import time
import urllib.parse

import d1_common.const
import d1_common.env
import d1_common.system_metadata
import d1_common.type_conversions
import d1_common.types.exceptions
import d1_common.util
import d1_common.xml

import d1_client.d1client
import d1_client.iter.sysmeta_multi

DEFAULT_TIMEOUT_SEC = 3 * 60
DEFAULT_N_WORKERS = 10


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--debug", action="store_true", help="Debug level logging")
    parser.add_argument(
        "--env",
        type=str,
        default="prod",
        help="Environment, one of {}".format(", ".join(d1_common.env.D1_ENV_DICT)),
    )
    parser.add_argument(
        "--cert-pub",
        dest="cert_pem_path",
        action="store",
        help="Path to PEM formatted public key of certificate",
    )
    parser.add_argument(
        "--cert-key",
        dest="cert_key_path",
        action="store",
        help="Path to PEM formatted private key of certificate",
    )
    parser.add_argument(
        "--timeout",
        action="store",
        default=d1_common.const.DEFAULT_HTTP_TIMEOUT,
        help="Amount of time to wait for calls to complete (seconds)",
    )

    args = parse_cmd_line()
    d1_common.util.log_setup(args.debug)
    events = d1_common.util.EventCounter()

    api_major = (
        args.major
        if args.major is not None
        else d1_client.d1client.get_api_major_by_base_url(args.baseurl)
    )

    try:
        if not os.path.isdir(args.dst_dir_path):
            raise SysMetaRetrieveError(
                'Not a valid directory. dst-path="{}"'.format(args.dst_dir_path)
            )
        _download_objects(
            args,
            api_major,
            events,
            args.timeout,
            args.cert_pem_path,
            args.cert_key_path,
        )
    except SysMetaRetrieveError as e:
        logging.error("Error: {}".format(str(e)))
    except d1_common.types.exceptions.DataONEException as e:
        logging.error("Node returned an error: {}".format(str(e)))
    except Exception:
        logging.error("Internal error: {}".format(str(e)))

    events.dump_to_log()


def parse_cmd_line():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.description = __doc__
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.add_argument("--debug", action="store_true", help="Debug level logging")
    parser.add_argument(
        "--cert-pub",
        dest="cert_pem_path",
        action="store",
        help="Path to PEM formatted public key of certificate",
    )
    parser.add_argument(
        "--cert-key",
        dest="cert_key_path",
        action="store",
        help="Path to PEM formatted private key of certificate",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        action="store",
        default=DEFAULT_TIMEOUT_SEC,
        help="Timeout for D1 API call to the source MN",
    )
    parser.add_argument(
        "--workers",
        type=int,
        action="store",
        default=DEFAULT_N_WORKERS,
        help="Max number of concurrent connections made to the source MN",
    )
    parser.add_argument(
        "--object-page-size",
        type=int,
        action="store",
        default=d1_common.const.DEFAULT_SLICE_SIZE,
        help="Number of objects to retrieve in each listObjects() call",
    )
    parser.add_argument(
        "--major",
        type=int,
        action="store",
        help="Use API major version instead of finding by connecting to CN",
    )
    parser.add_argument("baseurl", help="Source MN BaseURL")
    parser.add_argument(
        "dst_dir_path", help="Path to directory in which to store downloaded objects"
    )
    return parser.parse_args()


def _download_objects(args, api_major, events, timeout, cert_pem_path, cert_key_path):
    logging.info(
        'Downloading SysMeta and Science Objects from Node. baseurl="{}"'.format(
            args.baseurl
        )
    )

    sysmeta_iter = d1_client.iter.sysmeta_multi.SystemMetadataIteratorMulti(
        base_url=args.baseurl,
        page_size=args.object_page_size,
        max_workers=args.workers,
        max_result_queue_size=10,
        api_major=api_major,
        client_dict=_get_client_dict(timeout, cert_pem_path, cert_key_path),
        list_objects_dict=_get_list_objects_args_dict(),
    )
    start_sec = time.time()
    for i, sysmeta_pyxb in enumerate(sysmeta_iter):
        # if i > 100:
        #   break
        msg_str = "Error"
        if d1_common.system_metadata.is_sysmeta_pyxb(sysmeta_pyxb):
            pid = d1_common.xml.get_req_val(sysmeta_pyxb.identifier)
            try:
                _save_sysmeta(sysmeta_pyxb, pid, args.dst_dir_path)
                _download_source_sciobj_bytes(
                    args.baseurl,
                    api_major,
                    pid,
                    events,
                    args.dst_dir_path,
                    args.timeout,
                    args.cert_pem_path,
                    args.cert_key_path,
                )
            except d1_common.types.exceptions.DataONEException as e:
                logging.error(str(e))
            else:
                msg_str = pid
        elif d1_common.type_conversions.is_pyxb(sysmeta_pyxb):
            logging.error(d1_common.xml.serialize_to_xml_str(sysmeta_pyxb))
        else:
            logging.error(str(sysmeta_pyxb))

        _log_progress(
            events, "Importing objects", i, sysmeta_iter.total, msg_str, start_sec
        )


def _get_source_sysmeta(baseurl, api_major, pid, timeout, cert_pem_path, cert_key_path):
    client = _create_source_client(
        baseurl, api_major, timeout, cert_pem_path, cert_key_path
    )
    return client.getSystemMetadata(pid)


def _save_sysmeta(sysmeta_pyxb, pid, dst_dir_path):
    file_name = _get_safe_filename(pid, "sysmeta.xml")
    sysmeta_path = os.path.join(dst_dir_path, file_name)
    xml_str = d1_common.xml.serialize_pretty(sysmeta_pyxb)
    with open(sysmeta_path, "wb") as f:
        f.write(xml_str)


def _download_source_sciobj_bytes(
    baseurl, api_major, pid, events, dst_dir_path, timeout, cert_pem_path, cert_key_path
):
    file_name = _get_safe_filename(pid, "sciobj.bin")
    sciobj_path = os.path.join(dst_dir_path, file_name)
    if os.path.isfile(sciobj_path):
        events.log_and_count(
            "Skipped download of existing sciobj bytes",
            'pid="{}" path="{}"'.format(pid, sciobj_path),
        )
        return
    client = _create_source_client(
        baseurl, api_major, timeout, cert_pem_path, cert_key_path
    )
    client.get_and_save(pid, sciobj_path)


def _get_client_dict(timeout, cert_pem_path, cert_key_path):
    return {
        "timeout_sec": timeout,
        "verify_tls": False,
        "suppress_verify_warnings": True,
        "use_cache": False,
        "cert_pem_path": cert_pem_path,
        "cert_key_path": cert_key_path,
    }


def _get_list_objects_args_dict():
    return {
        # Restrict query for faster debugging
        # 'fromDate': datetime.datetime(2017, 1, 1),
        # 'toDate': datetime.datetime(2017, 1, 3),
    }


def _create_source_client(baseurl, api_major, timeout, cert_pem_path, cert_key_path):
    return d1_client.d1client.get_client_class_by_version_tag(api_major)(
        baseurl, **_get_client_dict(timeout, cert_pem_path, cert_key_path)
    )


def _assert_path_is_dir(dir_path):
    if not os.path.isdir(dir_path):
        raise SysMetaRetrieveError('Invalid dir path. path="{}"'.format(dir_path))


def _log_progress(event_counter, msg, i, n, pid, start_sec=None):
    if start_sec:
        elapsed_sec = time.time() - start_sec
        total_sec = float(n) / (i + 1) * elapsed_sec
        eta_sec = int(total_sec - elapsed_sec)
        s_int = eta_sec % 60
        eta_sec //= 60
        m_int = eta_sec % 60
        eta_sec //= 60
        h_int = eta_sec
        eta_str = " {}h{:02d}m{:02d}s".format(h_int, m_int, s_int)
    else:
        eta_str = ""
    logging.info(
        "{} - {}/{} ({:.2f}%{}) - {}".format(
            msg, i + 1, n, (i + 1) / float(n) * 100, eta_str, pid
        )
    )
    event_counter.count(msg)


def _get_safe_filename(pid, ext_str=None):
    return (
        urllib.parse.quote(pid.encode("utf-8"), safe=" @$,~*&") + ".{}".format(ext_str)
        if ext_str is not None
        else ""
    )


class SysMetaRetrieveError(Exception):
    pass


if __name__ == "__main__":
    sys.exit(main())
