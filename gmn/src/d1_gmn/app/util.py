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
"""General utilities."""

import inspect
import logging
import pprint
import traceback

import d1_common
import d1_common.const

import django.templatetags.static
import django.http

logger = logging.getLogger(__name__)


# noinspection PyProtectedMember
def coerce_put_post(request):
    """Django doesn't particularly understand REST. In case we send data over PUT,
    Django won't actually look at the data and load it. We need to twist its arm here.

    The try/except abomination here is due to a bug in mod_python. This should fix it.

    From django-piston/piston/utils.py

    """
    if request.method == "PUT":
        # Bug fix: if _load_post_and_files has already been called, for example by
        # middleware accessing request.POST, the below code to pretend the request
        # is a POST instead of a PUT will be too late to make a difference. Also
        # calling _load_post_and_files will result in the following exception:
        #
        #   AttributeError: You cannot set the upload handlers after the upload has
        #   been processed.
        #
        # The fix is to check for the presence of the _post field which is set the
        # first time _load_post_and_files is called (both by wsgi.py and
        # modpython.py). If it's set, the request has to be 'reset' to redo the
        # query value parsing in POST mode.
        if hasattr(request, "_post"):
            del request._post
            del request._files

        try:
            request.method = "POST"
            request._load_post_and_files()
            request.method = "PUT"
        except AttributeError:
            request.META["REQUEST_METHOD"] = "POST"
            request._load_post_and_files()
            request.META["REQUEST_METHOD"] = "PUT"

        request.PUT = request.POST


def dump_stack():
    frame = inspect.currentframe()
    stack_trace = traceback.format_stack(frame)
    logger.debug("".join(stack_trace))


def create_http_echo_response(request):
    logger.warning(
        "Echoing request (triggered by vendor extension or "
        "django.conf.settings.DEBUG_ECHO_REQUEST=True)"
    )
    return django.http.HttpResponse(
        pprint.pformat({"meta": request.META, "body": request.body}, indent=2),
        d1_common.const.CONTENT_TYPE_TEXT,
    )


def get_static_path(rel_path):
    return django.templatetags.static.static(rel_path)

