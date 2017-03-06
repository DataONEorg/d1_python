# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
"""Limit views to be called only with specific verbs

Decorator used on views to specify which verbs they may be called with. An
attempt to call the view with another verb causes a HttpResponseNotAllowed
response.
"""

from __future__ import absolute_import

# Django
import django.http


def allow_only_verbs(f, verbs):
  def wrap(request, *args, **kwargs):
    if request.method not in verbs:
      return django.http.HttpResponseNotAllowed(verbs)
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def get(f):
  return allow_only_verbs(f, ['GET'])


def head(f):
  return allow_only_verbs(f, ['HEAD'])


def put(f):
  return allow_only_verbs(f, ['PUT'])


def post(f):
  return allow_only_verbs(f, ['POST'])


def delete(f):
  return allow_only_verbs(f, ['DELETE'])
