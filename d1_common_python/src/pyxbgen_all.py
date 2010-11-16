#!/usr/bin/env python
'''Generate PyXB binding classes from schemas.

WARNING: Executing this script will overwrite content in d1_common/types/generated

To use::

  python pyxbgen_all schema_relative_path

where:

:schema_relative_path: 
  The relative path to current folder that contains the XML schema
  type definitions.
'''

import os
import sys
import glob


def generate_modules(schema_rel):
  #Find the schemas
  SCHEMA_SOURCE = os.path.abspath(schema_rel)
  if not os.path.exists(SCHEMA_SOURCE):
    print "Error: The specified path \"%s\" does not exist." % SCHEMA_SOURCE
    return

  OUTPUT_FOLDER = os.path.abspath('./d1_common/types/generated/')
  #Create the output folder if necessary
  if not os.path.exists(OUTPUT_FOLDER):
    os.mkdir(OUTPUT_FOLDER)

    #Delete any .py files on the output folder
  for generatedpy in glob.glob("%s/*.py" % OUTPUT_FOLDER):
    os.unlink(generatedpy)

  #Recreate the __init__.py file
  finit = file(os.path.abspath("%s/__init__.py" % OUTPUT_FOLDER), "w")
  finit.write("# Content in this folder is automatically generated using pyxbgen.\n")
  finit.write("# All edits will be lost on next generation.\n")
  finit.write("# ")
  finit.close()

  #cd to the location of the schemas
  cdir = os.getcwd()
  os.chdir(SCHEMA_SOURCE)
  args = []
  args.append('--binding-root=\'%s\'' % OUTPUT_FOLDER)
  #Note: the schema location should be updated with the release of the schema. 
  #If it's not, then the schema release is broken.
  #args.append('--location-prefix-rewrite=\'https://repository.dataone.org/software/cicore/tags/D1_SCHEMA_0_5/=./\'')

  for xsd in glob.glob("%s/*.xsd" % SCHEMA_SOURCE):
    schema = os.path.split(xsd)[1]
    if schema in ('common.xsd', 'dryadMetsAny.xsd', 'dryadXlink.xsd', 'dryadDim.xsd'):
      continue
    args.append('-u \'{0}\' -m \'{1}\''.format(schema, os.path.splitext(schema)[0]))

  cmd = 'pyxbgen {0}'.format(' '.join(args))
  print(cmd)
  os.system(cmd)
  os.chdir(cdir)


if __name__ == "__main__":
  if len(sys.argv) < 2:
    print __doc__
    sys.exit(1)
  generate_modules(sys.argv[1])
