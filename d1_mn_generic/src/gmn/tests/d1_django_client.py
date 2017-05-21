# # -*- coding: utf-8 -*-
#
# # This work was created by participants in the DataONE project, and is
# # jointly copyrighted by participating institutions in DataONE. For
# # more information on DataONE, see our web site at http://dataone.org.
# #
# #   Copyright 2009-2016 DataONE
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #   http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.
# """Test subject extraction from certificate and SubjectInfo"""
#
# from __future__ import absolute_import
#
#
# def use_django_test_client():
#   """Mock Requests to call the Django test client
#
#   Django includes a test framework with a test client that provides an interface
#   that's similar to that of an HTTP client, but calls Django internals directly.
#   The client enables most (but not all) functionality of a Django app to be
#   tested without actually starting the app as a network service.
#
#   For testing GMN's D1 REST interfaces, we want to issue the test requests via
#   the D1 MN client. Without it, we would have to reimplement much of what the D1
#   MN client does, related to generating and parsing D1 formatted REST
#   interactions.
#
#   The D1 MN client is based on the Requests library, so can only
#   """
#     with mock.patch('requests.Session.request', side_effect=self.mock_request):
#       print self.d1_client.getCapabilities()
#
#
#     self.d1_client = d1_client.mnclient_2_0.MemberNodeClient_2_0(
#       base_url='http://gmn/mn'
#     )
#
#     # self.d1_client._session.adapters = collections.OrderedDict()
#     # self.d1_client._session.mount('', DjangoResponseAdapter())
#     # Every test needs access to the request factory.
#     # self.factory = django.test.RequestFactory()
#     # self.user = User.objects.create_user(username='jacob', email='jacob@…',
#     # password='top_secret')
#
#   def mock_request(self, method, url, **kwargs):
#     url_path = url.replace('http://gmn/mn', '')
#     django_response = getattr(self.client, method.lower())(url_path, **kwargs)
#     self.assertIsInstance(django_response, django.http.response.HttpResponse)
#     return self.django_to_requests(method, url, django_response)
#
#   def django_to_requests(self, method, url, django_response):
#     """Build a Requests Response object from a Django HttpResponse
#     This only captures the info we need in order to mock the requests.
#     """
#     header_list = django_response.items()
#
#     u3_response = requests.packages.urllib3.HTTPResponse(
#       body=io.BytesIO(django_response.content),
#       headers=requests.packages.urllib3._collections.HTTPHeaderDict(header_list),
#       request_method=method,
#       status=django_response.status_code,
#       version='1/1',
#     )
#
#     prepared_request = requests.models.PreparedRequest()
#     prepared_request.prepare(
#       method=method,
#       url=url,
#     )
#
#     response = requests.Response()
#     response._content = django_response.content
#     response.status_code = django_response.status_code
#     response.headers = requests.structures.CaseInsensitiveDict(header_list)
#     response.raw = u3_response
#     response.reason = u3_response.reason
#     response.url = url
#     response.request = prepared_request
#
#     return response
