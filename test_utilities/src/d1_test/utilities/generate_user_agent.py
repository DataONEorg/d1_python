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
"""Return a randomly selected user agent string
"""
from __future__ import absolute_import

import random

USER_AGENTS = [
  'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6',
  'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
  'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322;'
  '.NET CLR 2.0.50727; .NET CLR 3.0.04506.30)',
  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
  'Mozilla/4.0 (compatible; MSIE 5.0; Windows NT 5.1; .NET CLR 1.1.4322)',
  'Opera/9.20 (Windows NT 6.0; U; en)',
  'Opera/9.00 (Windows NT 5.1; U; en)',
  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.50',
  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.0',
  'Mozilla/4.0 (compatible; MSIE 6.0; MSIE 5.5; Windows NT 5.1) Opera 7.02 [en]',
  'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20060127 Netscape/8.1',
  'Googlebot/2.1 ( http://www.googlebot.com/bot.html)',
  'Googlebot-Image/1.0 ( http://www.googlebot.com/bot.html)',
  'Mozilla/2.0 (compatible; Ask Jeeves)',
  'msnbot-Products/1.0 (+http://search.msn.com/msnbot.htm)',
]


def generate_random_user_agent():
  return random.choice(USER_AGENTS)
