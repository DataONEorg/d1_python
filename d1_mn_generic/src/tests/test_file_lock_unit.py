__author__ = 'mark'

import unittest
import service.mn.management.commands.process_replication_queue as rep_queue
import os
import subprocess


class TestFileLockUnit(unittest.TestCase):
  def test_file_acquire_lock(self):
    fname = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/tmp/test1.txt'
    subprocess.call(['python', 'acquire_file_lock.py'])

    try:
      with open(fname, 'w') as fp:
        fp.write(' 2')
    except IOError, e:
      print e.errno
      file_opened = False

    self.assertEqual(e, 'EBUSY')

  def test_file_release_lock(self):
    fname = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/tmp/test1.txt'
    subprocess.call(['python', 'acquire_release_file_lock.py'])
    try:
      with open(fname, 'w') as fp:
        fp.write(' 3')
    except:
      file_opened = False

    self.assertEqual(file_opened, True)


if __name__ == '__main__':
  unittest.main()
