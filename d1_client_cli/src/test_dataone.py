#!/usr/bin/env python

import os

args = []
args.append('--sysmeta-object-format bytes')
args.append('--sysmeta-submitter public')
args.append('--sysmeta-rightsholder somerightsholder')
args.append('--sysmeta-origin-member-node gmn-test')
args.append('--sysmeta-authoritative-member-node gmn-test')
#args.append('--mn-url https://demo1.test.dataone.org/knb/d1/mn/v1')
args.append('--mn-url https://localhost:443/mn/')

args.append('--cert-path roger.cert')
args.append('--key-path roger.key')

cmd = './dataone.py {0} create abc test.sciobj'.format(' '.join(args))
print cmd
os.system(cmd)
