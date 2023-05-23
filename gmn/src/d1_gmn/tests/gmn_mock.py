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
"""TODO: In Python 3, contextlib supports creating combined context managers
and decorators. django.test has a ContextDecorator class that works with Python
2. Follow the pattern there to convert all these to ContextDecorators.

TODO: In Python 3, items() is a view, so must use d.copy.items(), etc.

"""

import contextlib
import functools
import logging
import os

import mock
import pytest
import requests
import requests.exceptions

import django.test

import d1_gmn.tests

import d1_test.d1_test_case
import d1_test.instance_generator.random_data
import d1_gmn.app.proxy

logger = logging.getLogger(__name__)

# class DeContext(object):
#   """Makes a context manager also act as a decorator
#   https://stackoverflow.com/questions/9213600
#   """
#   def __init__(self, context_manager):
#     self._cm = context_manager
#
#   def __enter__(self):
#     return self._cm.__enter__()
#
#   def __exit__(self, *args, **kwds):
#     return self._cm.__exit__(*args, **kwds)
#
#   def __call__(self, func):
#     def wrapper(*args, **kwds):
#       with self:
#         return func(*args, **kwds)
#
#     return wrapper
#
# Usage:
# mydeco = Decontext(some_context_manager)

# Session and trusted subjects


@contextlib.contextmanager
def session_subjects_context(session_subject_set):
    """Override list of session subjects that GMN detects for authentication.

    the Session subjects is a list of DataONE subject strings for which the currently
    connected client is authenticated. Normally, the session subject list is derived
    from certificates and tokens passed by the client.

    """
    expanded_set = d1_test.d1_test_case.D1TestCase.expand_subjects(session_subject_set)
    logger.debug("ContextManager: session_subjects()")
    with mock.patch(
        "d1_gmn.app.middleware.view_handler.ViewHandler.get_session_subject_set",
        return_value=(sorted(expanded_set)[0], expanded_set),
    ):
        yield


@contextlib.contextmanager
def trusted_subjects_context(trusted_subject_set):
    """Override list of trusted subjects that GMN detects for authentication."""
    logger.debug("ContextManager: trusted_subjects()")
    with mock.patch(
        "d1_gmn.app.auth.get_trusted_subjects",
        return_value=d1_test.d1_test_case.D1TestCase.expand_subjects(
            trusted_subject_set
        ),
    ):
        yield


@contextlib.contextmanager
def whitelisted_subjects_context(whitelisted_subject_iter):
    """Override list of whitelists subjects that GMN detects as having access to create,
    update and delete APIs."""
    # def mock(request):
    #   return d1_test.d1_test_case.D1TestCase.expand_subjects(whitelisted_subject_set)
    logging.debug("ContextManager: whitelisted_subjects_context()")
    with mock.patch(
        "d1_gmn.app.auth.get_whitelisted_subject_set",
        return_value=d1_test.d1_test_case.D1TestCase.expand_subjects(
            whitelisted_subject_iter
        ),
    ):
        yield


# set_auth


def set_auth_decorator(func):
    @functools.wraps(func)
    def wrapper(
        session_subj_list,
        trusted_subj_list,
        whitelisted_subj_list,
        disable_auth,
        *args,
        **kwargs
    ):
        with set_auth_context(
            session_subj_list, trusted_subj_list, whitelisted_subj_list, disable_auth
        ):
            return func(*args, **kwargs)

    return wrapper


@contextlib.contextmanager
def set_auth_context(
    session_subj_list=None,
    trusted_subj_list=None,
    whitelisted_subj_list=None,
    do_disable_auth=False,
):
    """Set the session and trusted subjects for an GMN API call."""
    if do_disable_auth:
        with disable_auth():
            yield
    else:
        with session_subjects_context(session_subj_list):
            with trusted_subjects_context(trusted_subj_list):
                with whitelisted_subjects_context(whitelisted_subj_list):
                    yield


@contextlib.contextmanager
def isolated_whitelisted_subj():
    """Create a unique subject and override GMN auth so that the subject appears as
    single session and whitelisted, but not trusted, in API calls."""
    isolated_subj = "ISOLATED_{}".format(
        d1_test.instance_generator.random_data.random_subj(fixed_len=12)
    )
    with set_auth_context(
        session_subj_list=isolated_subj,
        trusted_subj_list=None,
        whitelisted_subj_list=isolated_subj,
        do_disable_auth=False,
    ):
        yield isolated_subj


@contextlib.contextmanager
def set_auth_context_with_defaults(
    session_subj_list=True,
    trusted_subj_list=True,
    whitelisted_subj_list=True,
    disable_auth=True,
):
    """Set the session, trusted and whitelisted subjects for an GMN API call.

    ``disable_auth``=True: The other subj lists are ignored and GMN sees all calls as
    coming from a fully trusted subject. ``param``=True: Use a default list of subjects.

    """
    with set_auth_context(
        ["session_subj_1", "session_subj_2", "session_subj_3"]
        if session_subj_list is True
        else session_subj_list,
        ["trusted_subj_1", "trusted_subj_2"]
        if trusted_subj_list is True
        else trusted_subj_list,
        ["whitelisted_subj_1", "whitelisted_subj_2"]
        if whitelisted_subj_list is True
        else whitelisted_subj_list,
        disable_auth,
    ):
        try:
            yield
        except requests.exceptions.ConnectionError as e:
            pytest.fail(
                "Check that the test function is decorated with "
                '"@responses.activate". error="{}"'.format(str(e))
            )


# -----------------

# disable_auth


@contextlib.contextmanager
def disable_auth():
    """Context manager that makes GMN think that all calls are issued by a fully trusted
    subject, "trusted_subj".

    This subject can call any API and received unfiltered results.

    """
    logging.debug("ContextManager: disable_auth()")
    with mock.patch(
        "d1_gmn.app.middleware.view_handler.ViewHandler.get_session_subject_set",
        return_value=("trusted_subj", {"trusted_subj"}),
    ):
        with mock.patch("d1_gmn.app.auth.is_trusted_subject", return_value=True):
            with mock.patch(
                "d1_gmn.app.auth.get_trusted_subjects_string",
                return_value="trusted_subj",
            ):
                yield


def no_client_trust_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with django.test.override_settings(
            TRUST_CLIENT_SUBMITTER=False,
            TRUST_CLIENT_ORIGINMEMBERNODE=False,
            TRUST_CLIENT_AUTHORITATIVEMEMBERNODE=False,
            TRUST_CLIENT_DATESYSMETADATAMODIFIED=False,
            TRUST_CLIENT_SERIALVERSION=False,
            TRUST_CLIENT_DATEUPLOADED=False,
        ):
            return func(*args, **kwargs)

    return wrapper


@contextlib.contextmanager
def disable_sysmeta_sanity_checks():
    with mock.patch("d1_gmn.app.views.assert_sysmeta.sanity"):
        yield


@contextlib.contextmanager
def disable_management_command_logging_setup():
    """Prevent management commands from setting up logging, which interferes with the
    logging that has already been set up by the test framework.
    """
    # logger = logging.getLogger()
    # d1_test.d1_test_case.logsetup()
    with mock.patch(
        "d1_gmn.app.mgmt_base.GMNCommandBase.setup_logging",
        return_value=logging.getLogger(""),
    ):
        # pytest.logsetup()
        yield


@contextlib.contextmanager
def disable_management_command_concurrent_instance_check():
    """Allow concurrent instances of the same management command."""
    with mock.patch("d1_gmn.app.mgmt_base.GMNCommandBase.using_single_instance"):
        yield


@contextlib.contextmanager
def disable_sciobj_store_write():
    """Prevent SciObj bytes from being stored in the SciObj store on disk."""
    logging.debug("ContextManager: disable_sciobj_store_write()")
    with mock.patch("d1_gmn.app.sciobj_store.open_sciobj_file_by_path"):
        yield os.devnull

@contextlib.contextmanager
def detect_proxy_auth():
    """"""
    logging.debug("ContextManager: detect_proxy_auth()")
    with mock.patch("d1_gmn.app.proxy._mk_http_basic_auth_header") as m:
        yield m
