__author__ = 'mark'
import os
import glob
import re
import shutil


def add_replication_policy(indir):
  # os.chdir(indir)
  path = os.path.join(indir, "*.sysmeta")
  p = re.compile('</identifier>')
  for filename in glob.glob(path):
    # filename = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/test_objects/5SLong(for5SShort).sysmeta'
    tmpfile = "temp.txt"
    with open(filename, "r") as fp:
      with open(tmpfile, "w") as fp2:
        line_iter = iter(fp)
        for line in line_iter:
          filepos = p.search(line)
          if filepos is not None:
            fp2.write(
              '''  <replicationPolicy replicationAllowed="true" numberReplicas="1">\n''' +
              '''  <preferredMemberNode>urn:node:mnTestFLYNN2</preferredMemberNode>\n''' +
              '''  </replicationPolicy>\n'''
            )

          fp2.write(line)
    shutil.move(tmpfile, filename)


def remove_replication_policy(indir):
  os.chdir(indir)
  for filename in glob.glob("*.sysmeta"):
    # filename = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/test_objects/5SLong(for5SShort).sysmeta'
    tmpfile = 'temp.txt'
    p1 = re.compile('<replicationPolicy')
    p2 = re.compile('<preferredMemberNode>')
    p3 = re.compile('</replicationPolicy>')
    with open(filename, 'r') as fp, open(tmpfile, "w") as out_fp:
      line_iter = iter(fp)
      for line in line_iter:
        filepos1 = p1.search(line)
        filepos2 = p2.search(line)
        filepos3 = p3.search(line)
        if filepos1 is None and filepos2 is None and filepos3 is None:
          out_fp.write(line)
    shutil.move(tmpfile, filename)


if __name__ == '__main__':
  indir = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/test_objects'
  add_replication_policy(indir)
