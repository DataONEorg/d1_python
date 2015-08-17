__author__ = 'mark'

import unittest
import service.mn.management.commands.process_replication_queue as rep_queue
import os
import subprocess
import fcntl
import tempfile
from mock import patch, PropertyMock
import django
from django.core.management.base import NoArgsCommand

# import tempfile


class ReplicationQueueProcessor():
  def __init__(self):
    pass

  def process_replication_queue(self):
    pass


class TestFileLockUnit(unittest.TestCase):
  # django.setup()
  def setUp(self):
    self.lock_file = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/test_file_lock_unit.single'

  def tearDown(self):
    try:
      os.remove(self.lock_file)
    except:
      pass

  def test_file_lock(self):
    fname = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/tmp/test1.txt'
    fp = open(fname)
    fcntl.flock(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    try:
      fcntl.flock(open(fname), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError, e:
      print e.errno
      file_opened = False
    finally:
      fcntl.flock(fp, fcntl.LOCK_UN)
    self.assertEqual(e.errno, 11)

  def test_process_queue_acquire_lock(self):
    lock_name = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/test_file_lock_unit.single'
    rp = rep_queue.Command()
    rp._acquire()
    new_rep_lock = rep_queue.Command()
    try:
      new_rep_lock._acquire()
    except IOError, e:
      print e.errno
    self.assertEqual(e.errno, 11)

  def test_process_queue_release_lock(self):
    lock_name = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/test_file_lock_unit.single'
    rp = rep_queue.Command()
    rp._acquire()
    new_rep_lock = rep_queue.Command()
    file_locked = True
    rp._release()
    try:
      new_rep_lock._acquire()
      file_locked = False
    except IOError, e:
      print e.errno
    self.assertFalse(file_locked)

  def test_acquire_assert_called_flock(self):
    with patch(
      'service.mn.management.commands.process_replication_queue.fcntl.flock'
    ) as mocked_method:
      lock_name = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/test_file_lock_unit.single'
      sng = rep_queue.Command()
      sng._acquire()
      mocked_method.assert_called_with(sng.handle, 6)

  @patch(
    'service.mn.management.commands.process_replication_queue.ReplicationQueueProcessor.process_replication_queue'
  )
  @patch(
    'service.mn.management.commands.process_replication_queue.ReplicationQueueProcessor'
  )
  def test_process_queue(self, mock_proc, mock_queue):
    with patch(
      'service.mn.management.commands.process_replication_queue.sys.exit'
    ) as mock_exit:
      lock_name = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/test_file_lock_unit.single'
      sng = rep_queue.Command()
      sng._acquire()
      new_sng = rep_queue.Command()
      try:
        new_sng.process_queue()
      except IOError, e:
        print e.errno
      self.assertFalse(new_sng.locked)

  def test_second_acquire_called_flock(self):
    with patch(
      'service.mn.management.commands.process_replication_queue.fcntl.flock'
    ) as mocked_method:
      lock_name = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/test_file_lock_unit.single'
      sng = rep_queue.Command()
      sng._acquire()
      sng._acquire()
      self.assertEqual(mocked_method.mock_calls[0], mocked_method.mock_calls[1])

  @patch(
    'service.mn.management.commands.process_replication_queue.ReplicationQueueProcessor.process_replication_queue'
  )
  @patch(
    'service.mn.management.commands.process_replication_queue.ReplicationQueueProcessor'
  )
  @patch(
    'service.mn.management.commands.process_replication_queue.Command._abort_if_stand_alone_instance'
  )
  @patch('service.mn.management.commands.process_replication_queue.Command._log_setup')
  def test_handle_noargs_called_abort(
    self, mock_log, mock_abort, mock_init, mock_process
  ):
    with patch(
      'service.mn.management.commands.process_replication_queue.Command._get_lock',
      new_callable=PropertyMock
    ) as mocked_method:
      cmd = rep_queue.Command()
      mock_init.return_value = ReplicationQueueProcessor()
      cmd.process_queue()
      mocked_method.assert_called_with()

  @patch(
    'service.mn.management.commands.process_replication_queue.ReplicationQueueProcessor.process_replication_queue'
  )
  @patch(
    'service.mn.management.commands.process_replication_queue.ReplicationQueueProcessor'
  )
  @patch('service.mn.management.commands.process_replication_queue.Command._get_lock')
  @patch('service.mn.management.commands.process_replication_queue.Command._log_setup')
  def test_handle_noargs_called_abort_if_stand_alone_instance(
    self, mock_log, mock_abort, mock_init, mock_process
  ):
    with patch(
      'service.mn.management.commands.process_replication_queue.Command._abort_if_stand_alone_instance',
      new_callable=PropertyMock
    ) as mocked_method:
      cmd = rep_queue.Command()
      mock_init.return_value = ReplicationQueueProcessor()
      cmd.process_queue()
      mocked_method.assert_called_with()

  @patch(
    'service.mn.management.commands.process_replication_queue.Command._abort_if_stand_alone_instance'
  )
  @patch(
    'service.mn.management.commands.process_replication_queue.ReplicationQueueProcessor.process_replication_queue'
  )
  @patch(
    'service.mn.management.commands.process_replication_queue.ReplicationQueueProcessor'
  )
  @patch('service.mn.management.commands.process_replication_queue.Command._log_setup')
  def test_handle_noargs_lock_acquired(
    self, mock_log, mock_init, mock_process, mock_abort
  ):
    cmd = rep_queue.Command()
    mock_init.return_value = ReplicationQueueProcessor()
    cmd.process_queue()
    self.assertEqual(
      cmd.filename,
      '/home/mark/d1/d1_python/d1_mn_generic/src/service/mn/management/commands/process_replication_queue.single'
    )


if __name__ == '__main__':
  unittest.main()
