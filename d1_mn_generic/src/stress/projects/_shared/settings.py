#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The GMN to stress test.
#BASEURL = 'https://localhost:8000'
BASEURL = 'https://192.168.1.51/mn'
#BASEURL = 'https://stress-1-unm.test.dataone.org/mn'
#BASEURL = 'https://stress-2-unm.test.dataone.org'
#BASEURL = 'https://gmn-dev.test.dataone.org/mn'

# Number of objects to retrieve with listObjects.
PAGESIZE = 1000

# If True, use client side certificates instead of GMN vendor specific
# extension.
USE_CERTS = True
