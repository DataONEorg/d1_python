#!/usr/bin/env python

import os
import re
import sys

sys.path.append('./build/lib.linux-x86_64-2.6/')
#print sys.path
import x509_extract_session

f = open('./cert_with_custom_ext.pem', 'rb')
print x509_extract_session.extract(f.read())
