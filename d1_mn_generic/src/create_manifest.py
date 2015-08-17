__author__ = 'mark'
import os
import sys
import subprocess

remove_list = ['MANIFEST', 'MANIFEST.in']
output = subprocess.check_output("svn list -R", shell=True)
print output
file_list = output.split('\n')
manifest_list = []
fname = 'MANIFEST.in'

exclude_list = [
  "tests/unicode_test.py", "tests/tweak_sysmeta.py", "tests/test_simple_client.py",
  "tests/rename_test.py", "tests/populate_valid_eml_docs.py",
  "tests/gmn_test_create_huge_file.py", "tests/gmn_clear.py", "tests/gen_sysmeta.py",
  "tests/fixcrc.py", "tests/add_random_access_policy.py",
  "service/test_systemMetadataChanged.py", "service/settings_site.py", "push_to_gmn_s.py",
  "push_to_gmn1.py", "fix_service_permissions.py"
]

with open(fname, 'w') as out:
  for item in exclude_list:
    out.write("exclude " + item + "\n")
  for item in file_list:
    if item not in remove_list and len(item) > 0 and item[-1] != '/':
      out.write("include " + item + "\n")
