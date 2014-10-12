#!/usr/bin/env python

# Create 512MB file: dd if=/dev/urandom of=big_file bs=1024 count=524288
#import cProfile

import d1_common.types.generated.dataoneTypes as dataoneTypes
import gmn_test_client


def generate_public_access_policy():
  accessPolicy = dataoneTypes.accessPolicy()
  accessRule = dataoneTypes.AccessRule()
  accessRule.subject.append('public')
  permission = dataoneTypes.Permission('read')
  accessRule.permission.append(permission)
  accessPolicy.append(accessRule)
  return accessPolicy


pid = 'big_file_4'

client = gmn_test_client.GMNTestClient('http://localhost:8000')

sysmeta = open('big_file.sysmeta', 'rb').read()
sysmeta_obj = dataoneTypes.CreateFromDocument(sysmeta)
sysmeta_obj.identifier = pid
sysmeta_obj.accessPolicy = generate_public_access_policy()

print sysmeta_obj.toxml()

with open('big_file', 'rb') as f:
  client.create(pid, f, sysmeta_obj)
  #cProfile.run('client.create("big_01", f, sysmeta_obj)', 'big_profile')
