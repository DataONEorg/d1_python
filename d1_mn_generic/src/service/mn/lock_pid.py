#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
''':mod:`lock_pid`
==================

:Synopsis:
  Block concurrent reads and updates on PIDs.
:Author: DataONE (dahl)
:Dependencies:
  - python 2.6
  
Does not require that the PID to be locked exists.
'''

# Stdlib.
import threading

# Django.
import django.utils.synch


class LockPID(object):
  '''PID based reader-writer lock with preference to writers.'''

  def __init__(self):
    self._pids = {}
    self._mutex = threading.Lock()

  def acquire_read(self, pid):
    with self._mutex:
      if pid not in self._pids:
        self._pids[pid] = django.utils.synch.RWLock()
      lock = self._pids[pid]
    lock.reader_enters()

  def acquire_write(self, pid):
    with self._mutex:
      if pid not in self._pids:
        self._pids[pid] = django.utils.synch.RWLock()
      lock = self._pids[pid]
    lock.writer_enters()

  def release_read(self, pid):
    lock = self._pids[pid]
    lock.reader_leaves()
    with self._mutex:
      if lock.active_readers == 0 and lock.active_writers == 0 and \
         lock.waiting_readers == 0 and lock.waiting_writers == 0:
        del self._pids[pid]

  def release_write(self, pid):
    lock = self._pids[pid]
    lock.writer_leaves()
    with self._mutex:
      if lock.active_readers == 0 and lock.active_writers == 0 and \
         lock.waiting_readers == 0 and lock.waiting_writers == 0:
        del self._pids[pid]

# Module scope dictionary of PID locks. Because modules get imported only
# once in Python, all the views will share this dictionary.
#
# TODO: Test to see if there are Apache deployment scenarios where multiple
# instances of this dictionary would be created. That would break the
# locking.
lock_pid = LockPID()

# ------------------------------------------------------------------------------
# Decorators.
# ------------------------------------------------------------------------------

# Decorators do PID based reader-writer lock with preference to writers.
#
# - Read on PID with ongoing read: concurrent
# - Read on PID with ongoing write: serialized
# - Write on PID with ongoing read: serialized
# - Write on PID with ongoing write: serialized
#
# It is implementation dependent if serialized threads are woken up in the same
# order in which they were blocked.
#
# The decorators require the first argument to be request and the second to
# be PID.


def for_read(f):
  def wrap(request, pid, *args, **kwargs):
    lock_pid.acquire_read(pid)
    try:
      return f(request, pid, *args, **kwargs)
    finally:
      lock_pid.release_read(pid)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def for_write(f):
  def wrap(request, pid, *args, **kwargs):
    lock_pid.acquire_write(pid)
    try:
      return f(request, pid, *args, **kwargs)
    finally:
      lock_pid.release_write(pid)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap
