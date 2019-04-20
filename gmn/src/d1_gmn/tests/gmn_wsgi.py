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

import contextlib

import django
import django.core.handlers.base
import django.core.handlers.wsgi

class WSGIClient(django.core.handlers.base.BaseHandler):
    """Submit requests to GMN directly via its WSGI interface.

    This client submits a raw WSGIRequest and returns the raw HttpResponse, both of
    which can contain streams.

    The test client that is bundled with Django collapses all streams to ``bytes``, both
    in requests and responses, so cannot be used for testing stream handling.
    """

    def __init__(self, django_settings_module=None, enforce_csrf_checks=True, *args, **kwargs):
        """Initialize the client and corresponding Django service.

        Args:
            django_settings_module: str
                Override the DJANGO_SETTINGS_MODULE environment variable setting.

                Requests will be sent to the Django service selected by the
                ``DJANGO_SETTINGS_MODULE`` environment variable. When running under
                pytest-django, the default value is set in ``tox.ini`.

            enforce_csrf_checks: bool
                Disable Cross Site Request Forgery protection.
        """
        django.setup(set_prefix=False)
        self.enforce_csrf_checks = enforce_csrf_checks
        super().__init__(*args, **kwargs)

    @contextlib.contextmanager
    def send_request(self, wsgi_environ_dict):
        """Send a WSGIRequest to a Django based service.

        Args:
            wsgi_environ_dict: dict
                WSGI environ dict from which to build a WSGIRequest.

                Example for ``MNStorage.create()``:

                    {
                        "REQUEST_METHOD": "POST",
                        "PATH_INFO": "/v2/object",
                        "CONTENT_TYPE": <content type of provided stream>,
                        "CONTENT_LENGTH": <length of provided stream>,
                        "REMOTE_ADDR": <IP or FQDN of *client*>,
                        "wsgi.input": <
                            MIME multipart stream providing the body of the
                            request
                        >,
                    }

        Returns:
            HttpResponse
        """
        # Set up middleware if needed. We couldn't do this earlier, because
        # settings weren't available.
        if self._middleware_chain is None:
            self.load_middleware()

        request = django.core.handlers.wsgi.WSGIRequest(wsgi_environ_dict)

        # sneaky little hack so that we can easily get round
        # CsrfViewMiddleware.  This makes life easier, and is probably
        # required for backwards compatibility with external tests against
        # admin views.
        request._dont_enforce_csrf_checks = not self.enforce_csrf_checks

        # Request goes through middleware.
        response = self.get_response(request)

        # Attach the originating request to the response so that it could be
        # later retrieved.
        response.wsgi_request = request

        yield response

        response.close()
